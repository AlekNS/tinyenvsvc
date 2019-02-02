create table users (
  id            serial primary key,
  email         varchar not null unique,
  password_hash varchar not null
);

create table stations (
  id   serial primary key,
  name varchar not null unique
);

create table parameters (
  id          serial primary key,
  name        varchar not null unique,
  description varchar not null default ''
);

create table measurements (
  id           bigserial primary key,
  station_id   int references stations(id) on update cascade on delete set null,
  parameter_id int references parameters(id) on update cascade on delete set null,
  measured_at  timestamp not null default now(),
  created_at   timestamp not null default now(),
  updated_at   timestamp,
  real_value   double precision not null default 0.0
); -- partition by range (measured_at); -- Need to be used

create index measurements_measured_at_inx_id_parameter on measurements (measured_at, parameter_id);

create or replace function date_trunc_epoch(src_date timestamp, trunc_interval interval)
returns timestamp as $$
  select (
    date_trunc('seconds', (src_date - timestamp 'epoch') / extract(epoch from trunc_interval)::integer)
     * extract(epoch from trunc_interval)::integer + timestamp 'epoch'
  );
$$ language sql immutable;
