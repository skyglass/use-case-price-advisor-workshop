FROM maven:3.9.9-eclipse-temurin-17 AS build
WORKDIR /workspace

COPY . .
RUN mvn -B -pl pricing-job -am -DskipTests package

# Flink 2.0.0, Scala 2.12, Java 17
FROM flink:2.0.0-scala_2.12-java17

COPY --from=build /workspace/pricing-job/target/pricing-job-*.jar /opt/flink/usrlib/pricing-job.jar
