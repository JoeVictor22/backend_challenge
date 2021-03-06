---
--  Cargos
---
insert into cargo (id, nome) values (1, 'administrador');
insert into cargo (id, nome) values (2, 'cliente');

---
--  Usuarios
---

insert into usuario (email, senha, cargo_id) values ('joelvictor1746@gmail.com', 'sha256$l2ygbSdF$2d03f994b4d99fdf6ca30832852826564189f3438a9f6abc7249bc74c08b7843', 1);


---
--  Controllers
---

insert into controller (id, nome) values (1, 'usuario');
insert into controller (id, nome) values (2, 'perfil');
insert into controller (id, nome) values (3, 'cargo');
insert into controller (id, nome) values (4, 'cidade');

---
--  Regras
---

--
--- administrator
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    1, 1, True);    -- /usuario/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   1, 1, True);    -- /usuario/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    1, 1, True);    -- /usuario/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   1, 1, True);    -- /usuario/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 1, 1, True);    -- /usuario/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    1, 2, True);    -- /perfil/allp
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   1, 2, True);    -- /perfil/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    1, 2, True);    -- /perfil/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   1, 2, True);    -- /perfil/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 1, 2, True);    -- /perfil/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    1, 3, True);    -- /cargo/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   1, 3, True);    -- /cargo/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    1, 3, True);    -- /cargo/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   1, 3, True);    -- /cargo/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 1, 3, True);    -- /cargo/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    1, 4, True);    -- /cidade/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   1, 4, True);    -- /cidade/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    1, 4, True);    -- /cidade/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   1, 4, True);    -- /cidade/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 1, 4, True);    -- /cidade/delete
--
--- cliente
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    2, 1, False);   -- /usuario/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   2, 1, True);    -- /usuario/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    2, 1, False);    -- /usuario/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   2, 1, True);    -- /usuario/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 2, 1, True);    -- /usuario/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    2, 2, False);   -- /perfil/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   2, 2, True);    -- /perfil/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    2, 2, False);    -- /perfil/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   2, 2, True);    -- /perfil/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 2, 2, False);    -- /perfil/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    2, 3, False);    -- /cargo/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   2, 3, False);    -- /cargo/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    2, 3, False);    -- /cargo/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   2, 3, False);    -- /cargo/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 2, 3, False);    -- /cargo/delete

INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('all',    2, 4, True);    -- /cidade/all
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('view',   2, 4, True);    -- /cidade/view
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('add',    2, 4, False);    -- /cidade/add
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('edit',   2, 4, False);    -- /cidade/edit
INSERT INTO public.regra(acao, cargo_id, controller_id, permitir) VALUES ('delete', 2, 4, False);    -- /cidade/delete