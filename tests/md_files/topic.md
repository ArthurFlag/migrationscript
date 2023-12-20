---
title: Add or remove customer contacts for your AWS custom cloud in Aiven
---

:::topic
**Custom clouds**

[Enable bring your own cloud (BYOC) with Aiven](/docs/platform/howto/byoc/enable-byoc).
:::

:::important
Custom cloud configuration in Aiven is an
[early availability feature](/docs/platform/concepts/beta_services). You cover the costs associated with building and
maintaining your custom cloud: payments for your integrated AWS
infrastructure and Aiven services within the custom cloud.
:::

This article details how to update the list of customer contacts for
your custom cloud using [Aiven Console](https://console.aiven.io/).

-   Administrator\'s role for your Aiven organization
-   At least one
    [custom cloud created](/docs/platform/howto/byoc/create-custom-cloud) in your Aiven organization
-   Access to [Aiven Console](https://console.aiven.io/)

## Update the contacts list

:::topic
**Result**

The list of contacts for your cloud has been updated.
:::

:::topic
**No superuser permissions and no `aiven_extras`? Migrate using the dump
method.**

Without superuser permissions or `aiven_extras` installed, you cannot
use the logical replication and migrate in a continuous manner. In that
case, you can migrate your database using the dump method if you have
the following permissions:

-   Connect
-   Select on all tables in the database
-   Select on all the sequences in the database
:::