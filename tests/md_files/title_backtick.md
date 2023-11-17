# `My title`

This article will show you how you can send logs from your Aiven service
to the AWS CloudWatch using the
`Aiven client </docs/tools/cli>`{.interpreted-text role="doc"}.

## Prerequisites

This is what you\'ll need to send your logs from the AWS CloudWatch
using the `Aiven client </docs/tools/cli>`{.interpreted-text
role="doc"}.

-   Aiven client installed.
-   An Aiven account with a service running.
-   An AWS account, and which region it is in.
-   An AWS Access Key and Secret Key. Generate the credentials by
    visiting **IAM dashboard** then click in **Users**, open the
    **Security credentials** tab, and choose **Create access key**.
    Click on **Download** as you will need this shortly.

Or, you can use the `avn`
`command-line tool </docs/tools/cli>`{.interpreted-text role="doc"} with
the following command:

    avn service user-creds-download --username <username> <service-name>

Read more: `../concepts/tls-ssl-certificates`{.interpreted-text
role="doc"}
