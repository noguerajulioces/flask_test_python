-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema examen
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema examen
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `examen` DEFAULT CHARACTER SET utf8 ;
USE `examen` ;

-- -----------------------------------------------------
-- Table `examen`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen`.`usuarios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(245) NULL,
  `apellido` VARCHAR(245) NULL,
  `email` VARCHAR(245) NULL,
  `password` VARCHAR(245) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examen`.`bandas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen`.`bandas` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(245) NULL,
  `socio_fundador` VARCHAR(245) NULL,
  `genero` VARCHAR(245) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examen`.`usuarios_has_bandas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen`.`usuarios_has_bandas` (
  `usuario_id` INT UNSIGNED NOT NULL,
  `banda_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`usuario_id`, `banda_id`),
  INDEX `fk_usuarios_has_bandas_bandas1_idx` (`banda_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_bandas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_bandas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `examen`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_bandas_bandas1`
    FOREIGN KEY (`banda_id`)
    REFERENCES `examen`.`bandas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
