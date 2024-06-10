-- Crear la base de datos si no existe
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'proyecto_musical') THEN
      CREATE DATABASE proyecto_musical;
   END IF;
END
$$;

-- Conectar a la base de datos proyecto_musical
\connect proyecto_musical;

-- Crear la tabla Datos si no existe
CREATE TABLE IF NOT EXISTS Datos (
    id SERIAL PRIMARY KEY,
    tecla VARCHAR(10) NOT NULL,
    nota_tecla VARCHAR(10) NOT NULL,
    frecuencia FLOAT NOT NULL,
    nota VARCHAR(10) NOT NULL,
    correcta BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
