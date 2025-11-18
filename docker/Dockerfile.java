FROM maven:3.9-eclipse-temurin-17

WORKDIR /app

# Copy generated tests project
COPY generated_tests/ .

# Pre-download Maven dependencies
RUN mvn dependency:go-offline -B

CMD ["mvn", "test"]
