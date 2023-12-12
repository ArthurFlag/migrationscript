::: note
::: title
Note
:::

For backups and restoration, Aiven utilises the popular Open Source
backup daemon `PGHoard <Terminology PGHoard>`{.interpreted-text
role="ref"}, which Aiven maintains. It makes real-time copies of
`WAL<Terminology PGWAL>`{.interpreted-text role="ref"} files to an
object store in compressed and encrypted format.
:::

You can also use the dedicated functions
[service logs](avn-service-logs) and
[service metrics](avn-service-metrics) to

Additionally, you have the option to
[export logs and metrics to an Aiven service or external provider](/docs/platform/concepts/logs-metrics-alerts), expanding your monitoring capabilities. For example:

-   You can send logs to
    [Aiven for Opensearch](/docs/products/opensearch).
-   You can send metrics to
    [Aiven for m3](/docs/products/m3db),
    and visualise these metrics with
    [Aiven for Grafana](/docs/products/grafana).

Or, you can use the `avn`
[command-line tool](/docs/tools/cli) with
the following command:

    avn service user-creds-download --username <username> <service-name>
