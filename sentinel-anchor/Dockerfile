# Stage 1: Build JAR using Maven
FROM maven:3.9.6-eclipse-temurin-21 AS builder
WORKDIR /build

COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Production JRE Runtime
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Non-root user for banking container security
RUN addgroup -S sentinel && adduser -S sentinel -G sentinel
USER sentinel

COPY --from=builder /build/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
