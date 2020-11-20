/*
数据产生表DataGen(此表虽是create table语句创建，但是为流表) ,可以根据规则生成数据 
参考Flink官方文档《DataGen SQL 连接器》shorturl.at/vKTX3
*/
create table datagen(id string, id2 int, id3 json)
tblproperties(
	'connector'='datagen',
	'fields.json.length'='4',
	'total-amount'='1000', --星环tdh自定义函数
	'row-per-second'='1000',
	'fields.id.length'='10');

/*
实时数据的低时延
*/
--将lantancyUDF.jar上传至HDFS，并且创建函数，该函数的作用是获取时延
add jar hdfs:/tmp/poc/latancyUDF.jar;
create temporary  function latancy as "latancyUDF"

--建立入流，指定topic以及zookeeper等，其中endtime字段是发数程序发完一条记录时的系统时间
create stream latancy_raw(
	id int,
	name string.
	age int,
	date timestamp,
	endtime bigint
)ROW FORMAT DELIMITED FIELDS TERMINATED by ',' 
tblproperties( "topic"="latancy", 
"kafka.zookeeper"="10.1.40.20:2181,10.1.40.21:2181,10.1.40.22:2181", 
"kafka.broker.list"="10.1.40.20:9092,10.1.40.21:9092,10.1.40.22:9092");

--创建流任务，使用latancy(endtime)来获得一条数据的处理延时
--其中latancy是求开始计算此条记录处理延时的函数，
--endtime是发送完此条记录的时间戳

create streamjob job_plain_latancy as(
"INSERT INTO table_latancy SELECT uniqu(),endtime,latancy(endtime) from latancy_raw"
)jobproperties("morphling.result.auto.flush"="true");

--建立结果接收表，其中latency字段是每条记录的处理延时
create table table_latancy(
	rowkey string,
	starttim bigint,
	latency bigint
)stored as hyperdrive;

--启动流任务
start streamjob job_plain_latancy;
select avg(latency) from table_latancy;


--窗口统计平均时延
--建立入流，指定topic以及zookeeper等，其中endtime字段是发数程序发完一条记录时的系统时间
create stream latancy_raw(
	id int,
	name string.
	age int,
	date timestamp,
	endtime bigint
)ROW FORMAT DELIMITED FIELDS TERMINATED by ',' 
tblproperties( "topic"="latancy1", 
"kafka.zookeeper"="10.1.40.20:2181,10.1.40.21:2181,10.1.40.22:2181", 
"kafka.broker.list"="10.1.40.20:9092,10.1.40.21:9092,10.1.40.22:9092");

/*
实时窗口时延
*/
--创建跳动窗口为3秒的衍生流
create stream windowAcc as select max(endtime) as maxtime from latancy_window
streamwindow w1 as (length '3' second slide '3' second) group by age;

--建立结果接收表，其中maxstartTime字段是窗口内最大的时间戳，windowendTime字段是窗口结束的时间戳
--windowsresultTime字段是窗口内数据出来完的时间戳，triggerLatency字段是窗口的延时
create table windowlatancy(
rowkey string,
maxstartTime bigint,
windowendTime bigint,
windowresultTime bigint,
triggerLatency bigint
)stored as hyperdrive

--建立统计窗口时延的流任务
create  streamjob job_window_latancy as (
"INSERT INTO windowlatancy SELECT uniqu(),maxtime,
(ceil(maxtime/1000))*1000,latancy(maxtime)+maxtime,
latancy(maxtime)+maxtime-(ceil(maxtime/1000)*1000)
from windowAcc")jobproperties("morphling.result.auto.flush"="true");

--启动流任务
start streamjob job_window_latancy;

select * from windowlatancy;
