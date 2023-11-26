# Загрузку набора данных произведем в DataFrame df. При этом обработка заголовка и вывод схемы будут выполнены
# автоматически.
from graphframes import GraphFrame

from pr5_tweets.spark.base import get_spark_session

spark = get_spark_session()

df = (
    spark.read.csv("file:///home/ivanovnp/tweets/ira_tweets_csv_hashed.csv", inferSchema=True, header=True)
)

# Создадим представление tw над DataFrame df.
df.createOrReplaceTempView("tw")

# Выполним очистку данных. Нас интересуют только те твиты, у которых ссылка на родительский твит в поле
# in_reply_to_tweetid имеет корректный формат: либо она нулевая, либо представляет последовательность из 18
# десятичных цифр, то есть корректный идентификатор твита. https://spark.apache.org/docs/2.3.0/api/sql/#rlike
cleaned_tweets = spark.sql(
    "select * from tw where in_reply_to_tweetid is null or in_reply_to_tweetid rlike '^\\\d{18}$'"
)
# Если ссылка нулевая, значит твит написан отдельно и не явлется ответом на другой твит. Такую ситуацию можно
# отследить проверкой в SQL is NULL. В противном случае твит является ответом на другой твит, и корректность
# идентификатора можно проверить конструкцией rlike, которая принимает регулярные выражения в стиле Java.

# Над очищенным DataFrame cleaned_tweets создадим представление ctw.
cleaned_tweets.createOrReplaceTempView("ctw")

# Зададим Vertex DataFrame. Вершиной графа будет твит. Выберем из набора данных только идентификаторы tweetid.
v = spark.sql("select tweetid as id from ctw")
# Зададим Edge DataFrame. Начальной вершиной ребра будет твит, определяемый своим идентикатором tweetid, а конечной -
# родительский твит, определяемый in_reply_to_tweetid.
e = spark.sql("select tweetid as src, in_reply_to_tweetid as dst from ctw")

# Теперь возможно инициализировать GraphFrame.

g = GraphFrame(v, e)

# Количество ребер входящих в вершину, соответствует количеству ответов на твит, который она представляет.
# Воспользуемся предопределенным DataFrame inDegrees, чтобы отсортировать вершины по убыванию величины полустепени
# захода.
g.inDegrees.orderBy("inDegree", ascending=False).show(10)

# Как оказалось, твитов, оставшихся без ответа, больше остальных. Виртуальный родительский твит с нулевым
# идентификатором соответствует виртуальной вершине с наибольшей полустепенью захода. Представляет интерес следующий
# в выборке твит, так как он является первым кандидатом на решение задачи. Выберем из набора данных все поля,
# указав его идентификатор.
spark.sql("select * from tw where tweetid = 816143852193124352").show()
# Это может показаться неожиданным, но выборка получилась пустой. Причина в том, что сам родительский твит в набор
# данных не вошел, в отличие от ответов на него. Сузим границы поиска только до тех родительских твитов, что попали в
# набор данных.

# Создадим одноименное представление для DataFrame inDegrees...
g.inDegrees.createOrReplaceTempView("inDegrees")
# ...и представление vertices для Vertex DataFrame.
v.createOrReplaceTempView("vertices")

# Выберем только те строки из inDegrees, для которых существует описание в Vertex DataFrame, то есть рассмотрим
# только те родительские твиты, что попали в набор данных. При этом выполним сортировку по убыванию величины
# полустепени захода вершины.
filteredInDegrees = spark.sql(
    "select * from inDegrees where exists (select vertices.id from vertices where vertices.id = inDegrees.id) order by inDegree desc"
)

# Искомая вершина будет первой в выборке. Воспользуемся функцией first(), чтобы адресовать первую строку DataFrame.
top_vertex = filteredInDegrees.first()


# Выберем из набора данных поля reply_count и tweet_text, указав идентификатор твита. Извлечь его из записи
# top_vertex можно по имени столбца.
spark.sql(
    "select tweetid, reply_count, tweet_text from ctw where tweetid = " + top_vertex.id
).show()

top_vertex.inDegree
# Равенство величины полустепени захода вершины и значения поля reply_count свидетельствует о том, что все ответы на
# данный твит вошли в набор данных.
