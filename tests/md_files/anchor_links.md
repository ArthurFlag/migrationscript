---
title: Enable OAUTH2/OIDC authentication for Aiven for Apache Kafka®
---

## Prerequisites

Aiven for Apache Kafka integrates with a wide range of OpenID Connect
identity providers (IdPs). However, the exact configuration steps can
differ based on your chosen IdP. Refer to your Identity Provider's
official documentation for specific configuration guidelines.

Before proceeding with the setup, ensure you have:

-   [Aiven for Apache Kafka®](/docs/products/kafka/getting-started) service running.
-   **Access to an OIDC provider**: Options include Auth0, Okta, Google
    Identity Platform, Azure, or any other OIDC compliant provider.
-   Required configuration details from your OIDC provider:
    -   **JWKS Endpoint URL**: URL to retrieve the JSON Web Key Set
        (JWKS).
    -   **Subject Claim Name**: Typically \"sub\"; however, this may
        vary with your OIDC provider.
    -   **Issuer URL or Identifier**: Identifies and verifies the JWT
        issuer.
    -   **Audience Identifier(s)**: Validates the JWT\'s intended
        recipients. For multiple audiences, make a note of all.

## Enable OAuth2/OIDC via Aiven Console {#console-authentication}

1.  In [Aiven Console](https://console.aiven.io/), select your project
    and then choose your Aiven for Apache Kafka® service.

2.  On the **Overview** page, scroll down to **Advanced configuration**
    and select **Configure**.

3.  In the **Advanced configuration** screen, select **Add configuration
    options**.

5.  Select **Save configurations** to save your changes

## Enable OAuth2/OIDC via Aiven CLI

To enable OAuth2/OIDC authentication for your Aiven for Apache Kafka
service using [Aiven CLI](/docs/tools/cli):

For detailed explanations on the OIDC parameters, refer to the
`console-authentication`{.interpreted-text role="ref"} section above.

Don't do anything `console-authentication <test>`{.interpreted-text role="ref"} section above.

## See also

-   Enable OAuth2/OIDC support for Apache Kafka® REST proxy
