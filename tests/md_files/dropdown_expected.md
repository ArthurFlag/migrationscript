Content

<details><summary>
Show the actors and actresses ordered by how many movies they are featured in
</summary>

``` sql
select
    actor.first_name,
    actor.last_name,
    count(actor.first_name) featured_count
from
    actor
left join film_actor on
    actor.actor_id = film_actor.actor_id
group by
    actor.first_name,
    actor.last_name
order by
    featured_count desc;
```

</details>

5.  In **Create PostgreSQL integration database** wizard, select one of
    the following options:
    -   To add an integration database to a service that is not yet
        integrated, go to the **New data service integration** tab.

        <details><summary>
        Expand for next steps
        </summary>

        1.  Select a service from the list of services available for
            integration.
        2.  Select **Continue**.
        3.  In the **Add integration databases** section, enter database
            names and schema names and select **Integrate & Create**
            when ready.

        You can preview the created databases by selecting **Databases
        and tables** from the sidebar.

        </details>
