FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /workspace

COPY . .
RUN mvn -B -pl banking-gateway -am -DskipTests package

FROM eclipse-temurin:21-jre
ENV JAVA_OPTS=""
WORKDIR /app
COPY --from=build /workspace/banking-gateway/target/banking-gateway-*.jar app.jar
EXPOSE 8079
ENTRYPOINT ["sh","-c","java $JAVA_OPTS -jar /app/app.jar"]
