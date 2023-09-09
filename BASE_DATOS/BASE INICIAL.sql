-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd_pensamientos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bd_pensamientos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd_pensamientos` DEFAULT CHARACTER SET utf8 ;
USE `bd_pensamientos` ;

-- -----------------------------------------------------
-- Table `bd_pensamientos`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_pensamientos`.`usuarios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(145) NOT NULL,
  `apellido` VARCHAR(145) NOT NULL,
  `email` VARCHAR(245) NOT NULL,
  `password` VARCHAR(245) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_pensamientos`.`pensamientos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_pensamientos`.`pensamientos` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pensamiento` VARCHAR(255) NOT NULL,
  `usuario_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_pensamientos_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_pensamientos_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `bd_pensamientos`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_pensamientos`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_pensamientos`.`likes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `usuario_id` INT UNSIGNED NOT NULL,
  `pensamiento_id` INT UNSIGNED NOT NULL,
  INDEX `fk_usuarios_has_pensamientos_pensamientos1_idx` (`pensamiento_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_pensamientos_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_usuarios_has_pensamientos_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `bd_pensamientos`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_usuarios_has_pensamientos_pensamientos1`
    FOREIGN KEY (`pensamiento_id`)
    REFERENCES `bd_pensamientos`.`pensamientos` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
