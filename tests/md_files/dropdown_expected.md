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

Content
