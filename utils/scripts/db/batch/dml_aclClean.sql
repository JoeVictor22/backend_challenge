delete from privileges;
delete from resources;
delete from actions;
delete from controllers;
delete from users;
delete from roles;

insert into roles (id, name) values (1, 'administrador');
insert into roles (id, name) values (2, 'usuário');

insert into users (username, password, role_id, email) values ('admin', 'sha256$l2ygbSdF$2d03f994b4d99fdf6ca30832852826564189f3438a9f6abc7249bc74c08b7843', 1, 'lucasssousa10@gmail.com');
insert into users (username, password, role_id, email) values ('user', 'sha256$l2ygbSdF$2d03f994b4d99fdf6ca30832852826564189f3438a9f6abc7249bc74c08b7843', 2, 'lucasssousa10@gmail.com');

insert into controllers (id, name) values (1, 'users');
insert into controllers (id, name) values (2, 'cidade');
insert into controllers (id, name) values (3, 'uf');

insert into actions (id, name) values (1, 'all');
insert into actions (id, name) values (2, 'view');
insert into actions (id, name) values (3, 'add');
insert into actions (id, name) values (4, 'edit');
insert into actions (id, name) values (5, 'delete');
insert into actions (id, name) values (6, 'download');

insert into resources (id, controller_id, action_id) values (  1, 1, 1);
insert into resources (id, controller_id, action_id) values (  2, 1, 2);
insert into resources (id, controller_id, action_id) values (  3, 1, 3);
insert into resources (id, controller_id, action_id) values (  4, 1, 4);
insert into resources (id, controller_id, action_id) values (  5, 1, 5);

insert into resources (id, controller_id, action_id) values (  6, 2, 1);
insert into resources (id, controller_id, action_id) values (  7, 2, 2);
insert into resources (id, controller_id, action_id) values (  8, 2, 3);
insert into resources (id, controller_id, action_id) values (  9, 2, 4);
insert into resources (id, controller_id, action_id) values ( 10, 2, 5);

insert into resources (id, controller_id, action_id) values ( 11, 3, 1);
insert into resources (id, controller_id, action_id) values ( 12, 3, 2);
insert into resources (id, controller_id, action_id) values ( 13, 3, 3);
insert into resources (id, controller_id, action_id) values ( 14, 3, 4);
insert into resources (id, controller_id, action_id) values ( 15, 3, 5);

insert into privileges (role_id, resource_id, allow) values (1, 1, true);
insert into privileges (role_id, resource_id, allow) values (1, 2, true);
insert into privileges (role_id, resource_id, allow) values (1, 3, true);
insert into privileges (role_id, resource_id, allow) values (1, 4, true);
insert into privileges (role_id, resource_id, allow) values (1, 5, true);

insert into privileges (role_id, resource_id, allow) values (1, 6, true);
insert into privileges (role_id, resource_id, allow) values (1, 7, true);
insert into privileges (role_id, resource_id, allow) values (1, 8, true);
insert into privileges (role_id, resource_id, allow) values (1, 9, true);
insert into privileges (role_id, resource_id, allow) values (1, 10, true);

insert into privileges (role_id, resource_id, allow) values (1, 11, true);
insert into privileges (role_id, resource_id, allow) values (1, 12, true);
insert into privileges (role_id, resource_id, allow) values (1, 13, true);
insert into privileges (role_id, resource_id, allow) values (1, 14, true);
insert into privileges (role_id, resource_id, allow) values (1, 15, true);

insert into privileges (role_id, resource_id, allow) values (2, 1, true);
insert into privileges (role_id, resource_id, allow) values (2, 2, true);
insert into privileges (role_id, resource_id, allow) values (2, 3, false);
insert into privileges (role_id, resource_id, allow) values (2, 4, true);
insert into privileges (role_id, resource_id, allow) values (2, 5, false);


insert into privileges (role_id, resource_id, allow) values (1, 6, true);
insert into privileges (role_id, resource_id, allow) values (1, 7, false);
insert into privileges (role_id, resource_id, allow) values (1, 8, false);
insert into privileges (role_id, resource_id, allow) values (1, 9, false);
insert into privileges (role_id, resource_id, allow) values (1, 10, false);

insert into privileges (role_id, resource_id, allow) values (1, 11, true);
insert into privileges (role_id, resource_id, allow) values (1, 12, false);
insert into privileges (role_id, resource_id, allow) values (1, 13, false);
insert into privileges (role_id, resource_id, allow) values (1, 14, false);
insert into privileges (role_id, resource_id, allow) values (1, 15, false);