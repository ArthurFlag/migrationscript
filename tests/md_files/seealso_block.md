# Aiven CLI

Aiven offers an installable CLI (command line interface) tool. You can
find it [on GitHub](https://github.com/aiven/aiven-client). Check out
[this blog](https://aiven.io/blog/aiven-cmdline) to learn how to use the
Aiven command line tool to do common tasks.

If you prefer to follow a video tutorial, check out this short video on
[how to get started](https://www.youtube.com/watch?v=nf3PPn5w6K8).

:::seealso
Test here
:::

## Getting started

:::important
Your AWS credentials should have appropriate access rights. According to
the official AWS documentation, the access rights required for the
credentials are:

-   \"logs:DescribeLogStreams\" which lists the log streams for the
    specified log group endpoint.
-   \"logs:CreateLogGroup\" which creates a log group with the specified
    name endpoint.
-   \"logs:CreateLogStream\" which creates a log stream for the
    specified log group.
-   \"logs:PutLogEvents\" which uploads a batch of log events to the
    specified log stream.

:::seealso
Find more information about [CloudWatch
API](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_Operations.html).
:::
:::