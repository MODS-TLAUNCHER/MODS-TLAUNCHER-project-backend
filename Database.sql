CREATE SCHEMA bienestar;

SET search_path TO bienestar;

CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);


CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    correo_institucional VARCHAR(150) UNIQUE NOT NULL,
    correo_alternativo VARCHAR(150),
    password_hash VARCHAR(255) NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    correo_verificado BOOLEAN DEFAULT FALSE,
    carrera VARCHAR(100),
    creditos INT DEFAULT 0,
    meta TEXT,
    nivel_estres INT CHECK (nivel_estres BETWEEN 1 AND 5),
    activo BOOLEAN DEFAULT TRUE,
    rol_id INT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (rol_id)
        REFERENCES rol(id)
);

CREATE TABLE recuperacion_cuenta (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_recuperacion_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);


CREATE TABLE habito (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(50),
    descripcion TEXT
);


CREATE TABLE registro_diario (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    estado_animo VARCHAR(50),
    comentario VARCHAR(255),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_registro_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);


CREATE TABLE registro_habito (
    id SERIAL PRIMARY KEY,
    registro_id INT NOT NULL,
    habito_id INT NOT NULL,
    valor INT NOT NULL,

    CONSTRAINT fk_registrohabito_registro
        FOREIGN KEY (registro_id)
        REFERENCES registro_diario(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_registrohabito_habito
        FOREIGN KEY (habito_id)
        REFERENCES habito(id)
);


CREATE TABLE reporte (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    semana INT NOT NULL,
    anio INT NOT NULL,
    promedio_sueno FLOAT,
    promedio_agua FLOAT,
    promedio_actividad FLOAT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reporte_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);


CREATE TABLE recordatorio (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    hora TIME NOT NULL,
    mensaje VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_recordatorio_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);


CREATE TABLE retroalimentacion (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_retro_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);


CREATE TABLE recurso_apoyo (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),
    url VARCHAR(255),
    creado_por INT,

    CONSTRAINT fk_recurso_usuario
        FOREIGN KEY (creado_por)
        REFERENCES usuario(id)
);
