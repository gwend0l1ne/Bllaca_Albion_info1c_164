-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: zzz_xxxxx_NOM_PRENOM_INFO1X_SUJET_104_2021

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS zxzx_crud_tot_NOM_PRENOM_INFO1X_SUJET_164_2022;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS zxzx_crud_tot_NOM_PRENOM_INFO1X_SUJET_164_2022;

-- Utilisation de cette base de donnée

USE zxzx_crud_tot_NOM_PRENOM_INFO1X_SUJET_164_2022;
-- --------------------------------------------------------

--
-- Structure de la table `t_livre`
--

CREATE TABLE `t_livre` (
  `id_livre` int(11) NOT NULL,
  `nom_livre` varchar(255) DEFAULT NULL,
  `page_livre` int(11) DEFAULT NULL,
  `description_livre` text COMMENT 'Résume du livre',
  `cover_link_livre` text COMMENT 'lien photo couverture du livre',
  `date_sortie_livre` date DEFAULT NULL COMMENT 'date sortie du livre'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_livre`
--




--
-- Structure de la table `t_genre`
--

CREATE TABLE `t_genre` (
  `id_genre` int(11) NOT NULL,
  `intitule_genre` varchar(50) DEFAULT NULL,
  `date_ins_genre` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_genre`
--

INSERT INTO `t_genre` (`id_genre`, `intitule_genre`, `date_ins_genre`) VALUES
(1, 'action', '2022-06-10 09:49:7'),
(2, 'drame', '2022-06-10 09:49:7'),
(3, 'comedie', '2022-06-10 09:49:7'),
(4, 'aventure', '2022-06-10 09:49:7'),
(5, 'fantasie', '2022-06-10 09:49:7'),
(6, 'science fiction', '2022-06-10 09:49:7'),
(7, 'romantique', '2022-06-10 09:49:7'),
(8, 'horreur', '2022-06-10 09:49:7'),
(9, 'historique', '2022-06-10 09:49:7'),
(10, 'crime', '2022-06-10 09:49:7'),
(11, 'réalisme', '2022-06-10 09:49:7'),
(12, 'mystere', '2022-06-10 09:49:7'),
(13, 'philosophique', '2022-06-10 09:49:7'),
(14, 'western', '2022-06-10 09:49:7'),
(15, 'anime', '2022-06-10 09:49:7'),
(16, 'cartoon', '2022-06-10 09:49:7'),
(17, 'roman', '2022-06-10 09:49:7');

-- --------------------------------------------------------

--
-- creation table 'auteur'
--

CREATE TABLE `auteur` (
  `id_auteur` INT NOT NULL,
  `nom_auteur` VARCHAR(45) NULL,
  `prenom_auteur` VARCHAR(45) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- contenu de la table 'auteur'
--



-- --------------------------------------------------------


--
-- Structure de la table `t_genre_livre`
--

CREATE TABLE `t_genre_livre` (
  `id_genre_livre` int(11) NOT NULL,
  `fk_genre` int(11) DEFAULT NULL,
  `fk_livre` int(11) DEFAULT NULL,
  `fk_auteur` int(11) DEFAULT NULL,
  `date_insert_genre` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_genre_livre`
--




--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_livre`
--
ALTER TABLE `t_livre`
  ADD PRIMARY KEY (`id_livre`);

--
-- Index pour la table `t_genre`
--
ALTER TABLE `t_genre`
  ADD PRIMARY KEY (`id_genre`),
  ADD UNIQUE KEY `intitule_genre` (`intitule_genre`);

ALTER TABLE `auteur`
  ADD PRIMARY KEY (`id_auteur`);

ALTER TABLE `auteur`
  MODIFY `id_auteur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Index pour la table `t_genre_livre`
--
ALTER TABLE `t_genre_livre`
  ADD PRIMARY KEY (`id_genre_livre`),
  ADD KEY `fk_genre` (`fk_genre`),
  ADD KEY `fk_livre` (`fk_livre`),
  ADD KEY `fk_auteur` (`fk_auteur`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_livre`
--
ALTER TABLE `t_livre`
  MODIFY `id_livre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT pour la table `t_genre`
--
ALTER TABLE `t_genre`
  MODIFY `id_genre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT pour la table `t_genre_livre`
--
ALTER TABLE `t_genre_livre`
  MODIFY `id_genre_livre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;
--
-- Contraintes pour les tables exportées
--



--
-- Contraintes pour la table `t_genre_livre`
--
ALTER TABLE `t_genre_livre`
  ADD CONSTRAINT `t_genre_livre_ibfk_1` FOREIGN KEY (`fk_genre`) REFERENCES `t_genre` (`id_genre`),
  ADD CONSTRAINT `t_genre_livre_ibfk_2` FOREIGN KEY (`fk_livre`) REFERENCES `t_livre` (`id_livre`),
  ADD CONSTRAINT `t_genre_livre_ibfk_3` FOREIGN KEY (`fk_auteur`) REFERENCES `auteur` (`id_auteur`);

--
-- contrainte pour la table "auteur"
--

INSERT INTO `t_livre` (`id_livre`, `nom_livre`, `page_livre`, `description_livre`, `cover_link_livre`, `date_sortie_livre`) VALUES
(1, 'Nouvelles histoires magiques', 316, 'Louis Pauwels et Guy Breton continuent de scruter l`envers mystérieux de notre histoire. Dans ces Nouvelles Histoires magiques (tirées de leur célèbre émission de France-Inter), ils se penchent une fois de plus sur des phénomènes inexpliqués : vision','https://images-na.ssl-images-amazon.com/images/I/519Y4Z4FJZL._SX210_.jpg', '2000-01-01'),
(2, 'World War Z', 544, 'La guerre des Zombies a eu lieu, et elle a failli éradiquer l\'ensemble de l\'humanité.L\'auteur, en mission pour l\'ONU - ou ce qu\'il en reste - et poussé par l\'urgence de préserver les témoignages directs des survivants de ces années apocalyptiques, a voyagé dans le monde entier pour les rencontrer, des cités en ruine qui jadis abritaient des millions d\'âmes jusqu\'aux coins les plus inhospitaliers de la planète. Il a recueilli les paroles d\'hommes, de femmes, parfois d\'enfants, ayant dû faire face à l\'horreur ultime. Jamais auparavant nous n\'avions eu accès à un document de première main aussi saisissant sur la réalité de l\'existence - de la survivance - humaine au cours de ces années maudites.Depuis le désormais tristement célèbre village de Nouveau-Dachang, en Chine, là où l\'épidémie a débuté avec un patient zéro de douze ans, jusqu\'aux forêts du Nord dans lesquelles - à quel prix ! - nombre d\'entre nous ont trouvé refuge, en passant par les Etats-Unis d\'Afrique du Sud où a été élaboré l\'odieux plan Redecker qui finirait pourtant par sauver l\'humanité, cette chronique des années de guerre reflète sans faux-semblants la réalité de l\'épidémie. Prendre connaissance de ces comptes-rendus parfois à la limite du supportable demandera un certain courage au lecteur. Mais l\'effort en vaut la peine, car rien ne dit que la Ze Guerre mondiale sera la dernière.', 'https://images-na.ssl-images-amazon.com/images/I/414TkffpQxL._SX210_.jpg', '2010-11-03'),
(3, 'Le travail du furet', 515, 'La maladie a été éradiquée par la science. Pour maintenir un certain niveau de vie et éviter la surpopulation, des tueurs mandatés par l\'Etat doivent éliminer 400 000 personnes chaque année. Riche, pauvre, homme, femme, personne n\'y échappe. Mais les victimes sont-elles vraiment désignées au hasard ? C\'est lorsque le Furet commence à en douter que les ennuis lui tombent dessus. Aura-t-il la force de se rebeller ? Livre culte, naviguant entre polar et dystopie, Le Travail du Furet est un roman coup-de-poing, sans concession sur les dérives de nos sociétés. Il est ici accompagné de sept nouvelles qui lui font écho et qui sont autant de cris d\'alarme pour notre avenir. Retrouvez également, pour la première fois publié, le synopsis du tome 2 qui n\'a jamais vu le jour.', 'https://images-na.ssl-images-amazon.com/images/I/51p%2Bfy8zRFL._SX195_.jpg', '2015-03-09');


INSERT INTO `auteur`(`id_auteur`,`prenom_auteur`,`nom_auteur`) VALUES
(1,"Max","brooks"),
(2,"Jean-Pierre","Andrevone"),
(3,"Guy","Breton"),
(4,"Pierre","Zaccone"),
(5,"Edmond","Jabès"),
(6,"Victor","Hugo"),
(7,"André","Aciman");


INSERT INTO `t_genre_livre` (`id_genre_livre`, `fk_genre`, `fk_livre`,`fk_auteur`, `date_insert_genre`) VALUES
(141, 14, 1, 3, '2020-02-12 19:30:33'),
(144, 4, 2, 1, '2020-02-12 19:35:59'),
(145, 1, 3, 2, '2020-02-12 19:36:57');