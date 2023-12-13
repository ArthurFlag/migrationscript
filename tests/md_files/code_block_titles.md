
-   Allow remote connections on the source database.

    Log in to the server hosting your database and the MySQL
    installation. Next, open the network configuration of MySQL with the
    following command:

    ``` bash
    sudo code /etc/mysql/mysql.conf.d/mysqld.cnf
    ```

    ``` {.bash caption="Expected output"}
    . . .
    lc-messages-dir = /usr/share/mysql
    skip-external-locking
    #
    # Instead of skip-networking the default is now to listen only on
    # localhost which is more compatible and is not less secure.
    bind-address            = 127.0.0.1
    . . .
    ```

Test