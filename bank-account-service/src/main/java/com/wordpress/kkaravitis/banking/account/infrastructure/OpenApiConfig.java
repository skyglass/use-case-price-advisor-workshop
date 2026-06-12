package com.wordpress.kkaravitis.banking.account.infrastructure;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.OAuthFlow;
import io.swagger.v3.oas.models.security.OAuthFlows;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    OpenAPI accountOpenApi() {
        return new OpenAPI()
              .info(new Info()
                    .title("Banking Account API")
                    .version("v1"))
              .components(new Components()
                    .addSecuritySchemes("oauth2-password", oauth2PasswordScheme()))
              .addSecurityItem(new SecurityRequirement().addList("oauth2-password"));
    }

    private SecurityScheme oauth2PasswordScheme() {
        return new SecurityScheme()
              .type(SecurityScheme.Type.OAUTH2)
              .flows(new OAuthFlows()
                    .password(new OAuthFlow()
                          .tokenUrl("/auth/token")));
    }
}
