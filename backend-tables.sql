CREATE TABLE `user_account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  `last_login` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE org (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL, -- owner

    title VARCHAR(255) NOT NULL,
    description TEXT,
    email VARCHAR(150),
    phone VARCHAR(15),
    address TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_org_user
        FOREIGN KEY (user_id) REFERENCES user_account(id)
        ON DELETE CASCADE
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL, -- creator
    org_id BIGINT NOT NULL,

    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_user
        FOREIGN KEY (user_id) REFERENCES user_account(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_users_org
        FOREIGN KEY (org_id) REFERENCES org(id)
        ON DELETE CASCADE
);

CREATE TABLE roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,
    org_id BIGINT NOT NULL,

    name VARCHAR(100) NOT NULL,
    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_roles_user
        FOREIGN KEY (user_id) REFERENCES user_account(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_roles_org
        FOREIGN KEY (org_id) REFERENCES org(id)
        ON DELETE CASCADE
);

CREATE TABLE teams (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,
    org_id BIGINT NOT NULL,

    name VARCHAR(255) NOT NULL,
    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_teams_user
        FOREIGN KEY (user_id) REFERENCES user_account(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_teams_org
        FOREIGN KEY (org_id) REFERENCES org(id)
        ON DELETE CASCADE
);

CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,
    org_id BIGINT NOT NULL,

    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_projects_user
        FOREIGN KEY (user_id) REFERENCES user_account(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_projects_org
        FOREIGN KEY (org_id) REFERENCES org(id)
        ON DELETE CASCADE
);

CREATE TABLE team_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    team_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,

    CONSTRAINT fk_tm_team
        FOREIGN KEY (team_id) REFERENCES teams(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tm_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE (team_id, user_id)
);

CREATE TABLE project_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    project_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,

    role VARCHAR(50) DEFAULT 'CONTRIBUTOR',

    CONSTRAINT fk_pm_project
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pm_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE (project_id, user_id)
);