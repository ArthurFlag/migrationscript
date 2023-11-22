
## Code

1.  Create a new file named `main.go` and add the following content:

    ::: {.literalinclude language="go"}
    /code/products/cassandra/connect.go
    :::

    This code first creates a keyspace named `example_keyspace` and a
    table named `example_go` that contains an `id` and a `message`.
    Then, it writes a new entry into the table with the values `1` and
    `hello world`. Finally, it reads the entry from the table and prints
    it.

2.  Execute the following from a terminal window to build an executable:

    ``` 
    go build main.go
    ```