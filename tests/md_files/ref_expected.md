---
title: Log integration with Loggly
---

Your logs should now be visible on Loggly **Search** tab. Enter the tag
name your previously specified (e.g. `tag:your-tag` ) and it will
populate the dashboard with the log events from the Aiven service.

:::tip
You can automate the creation of the Loggly integration using the
[Aiven CLI dedicated command](/docs/myfolder/mypage#avn_service_integration_create).
:::

For detailed explanations on the OIDC parameters, refer to the
[Assign standalone](#title) section above.

### Assign standalone {#title}

To assign a standalone project to an organization or unit use the
following call. Replace `ACCOUNT_ID` with the ID of the organization or
unit and `PROJECT_NAME` with the name of the project to assign.

### Create an organization {#create-org-api}

Content