# Price Advisor And Banking Workshop

This repository contains one combined application:

- Angular UI served by Nginx.
- Spring Cloud Gateway as the single public REST and Swagger endpoint.
- Pricing Advisor services: pricing API, Flink pricing job, and Python model API.
- Banking services imported from the event-driven banking workshop: account, transfer, anti-fraud, outbox, inbox, and shared API modules.
- Keycloak with an automatically imported realm for local OAuth2 testing.
- Kafka, Kafka Connect, Debezium, PostgreSQL, Flink, Kafdrop, and PgAdmin.

The Java modules are built from one Maven parent project at the repository root.

## Requirements

- Docker with the Docker Compose plugin.
- Free local ports: `2181`, `5050`, `5432`, `5433`, `5434`, `5435`, `7000`, `7070`, `8079`, `8083`, `8088`, `8180`, `9001`, and `9092`.

The first startup builds Docker images and downloads Maven, npm, Python, and base-image dependencies.

## Start The Application

From the repository root:

```bash
docker compose up --build -d
```

Watch startup logs if needed:

```bash
docker compose logs -f banking-gateway pricing-api bank-transfer-service bank-account-service ui
```

Useful URLs:

- UI: http://localhost:7000
- Gateway health: http://localhost:8079/actuator/health
- Swagger UI: http://localhost:8079/swagger-ui.html
- Pricing model API docs: http://localhost:7070/docs
- Flink dashboard: http://localhost:8088
- Kafdrop: http://localhost:9001
- Kafka Connect: http://localhost:8083
- PgAdmin: http://localhost:5050
- Keycloak admin console: http://localhost:8180

PgAdmin login:

- Email: `admin@priceadvisor.dev`
- Password: `admin`

Keycloak admin login:

- Username: `admin`
- Password: `admin`

## Application Login

Use the login form in the top-right of the UI:

- Client ID: `price-advisor-ui`
- Username: `alice`
- Password: `password`

The UI uses the Gateway token endpoint and sends OAuth2 bearer tokens to the API routes. The pricing and banking screens are separated in the UI; pricing advisor functionality is independent from banking accounts and transfers.

Additional test user:

- Client ID: `price-advisor-ui`
- Username: `bob`
- Password: `password`

Seeded banking data:

- `alice` has customer ID `CC-200` and account `ACC-201`.
- `bob` has customer ID `CC-201` and account `ACC-101`.

## Swagger UI

Open:

```text
http://localhost:8079/swagger-ui.html
```

The service selector in the top-right lets you choose:

- `pricing advisor`
- `banking`
- `transfer`

To call secured endpoints from Swagger:

1. Select a service from the top-right menu.
2. Click `Authorize`.
3. Use the OAuth2 password form.
4. Enter client ID `price-advisor-ui`, username `alice`, and password `password`.
5. Leave client secret and scopes empty.

Swagger sends the password grant to the Gateway at `/auth/token`; the Gateway forwards it to Keycloak. For transfer calls, the Gateway performs token exchange before routing to the transfer service.

## Public Gateway Routes

All browser and Swagger traffic goes through Spring Cloud Gateway on port `8079`:

- Pricing API: `http://localhost:8079/api/pricing-advisor/pricing`
- Competitor prices API: `http://localhost:8079/api/pricing-advisor/competitor`
- Pricing WebSocket/SockJS: `http://localhost:8079/api/pricing-advisor/ws`
- Banking accounts API: `http://localhost:8079/api/banking/accounts`
- Transfer API: `http://localhost:8079/api/transfer`
- Token endpoint: `http://localhost:8079/auth/token`

## Keycloak Configuration

Keycloak is configured automatically during Compose startup from:

```text
config/keycloak/realm-banking.json
```

No manual Keycloak setup is required for local testing. If you change the realm import and need Keycloak to import it from scratch, reset volumes:

```bash
docker compose down -v
docker compose up --build -d
```

## Publish A Pricing Model

The model API can train/export the model and publish it to Kafka:

```bash
curl -X POST http://localhost:7070/pipeline/run
```

## Stop The Application

Stop containers while keeping persisted volumes:

```bash
docker compose down
```

Stop containers and remove persisted database, Kafka, and Keycloak state:

```bash
docker compose down -v
```

## Java Maven Project

Build all Java modules:

```bash
mvn clean package
```

Build without tests:

```bash
mvn -DskipTests package
```

Build the gateway and required reactor modules:

```bash
mvn -pl banking-gateway -am package
```
