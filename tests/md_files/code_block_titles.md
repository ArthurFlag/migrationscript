
-   Allow remote connections on the source database.

    following command:

    ``` bash
    sudo code /etc/mysql/mysql.conf.d/mysqld.cnf
    ```

    ``` {.bash caption="Expected output"}
    . . .
    lc-messages-dir = /usr/share/mysql
    skip-external-locking
    . . .
    ```
    Test

    ``` {.bash caption="Expected output"}
    . . .
    lc-messages-dir = /usr/share/mysql
    skip-external-locking
    bind-address            = *
    . . .
    ```

    Save the changes and exit the file. Restart MySQL to apply the
    changes.

    ``` bash
    sudo systemctl restart mysql
    ```