-- MySQL Script generated by MySQL Workbench
-- Sat Apr 26 17:08:57 2025
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema carbonemissionscalculator
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema carbonemissionscalculator
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `carbonemissionscalculator` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `carbonemissionscalculator` ;

-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`user_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`user_details` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `forename` VARCHAR(30) NOT NULL,
  `surname` VARCHAR(30) NOT NULL,
  `dob` DATE NOT NULL,
  `password` VARCHAR(250) NOT NULL,
  `email` VARCHAR(250) NOT NULL,
  `security_question` VARCHAR(250) NULL DEFAULT NULL,
  `security_answer` VARCHAR(250) NULL DEFAULT NULL,
  `locked` INT NOT NULL DEFAULT '0',
  `linked_accounts` VARCHAR(250) NULL DEFAULT NULL,
  `pending_links` VARCHAR(250) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 26
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`appliance_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`appliance_logs` (
  `log_number` INT NOT NULL AUTO_INCREMENT,
  `total_emissions` FLOAT NOT NULL,
  `date` DATE NOT NULL,
  `oven` FLOAT NOT NULL,
  `lighting` FLOAT NOT NULL,
  `fridge` FLOAT NOT NULL,
  `heating` FLOAT NOT NULL,
  `phones` FLOAT NOT NULL,
  `pc` FLOAT NOT NULL,
  `tv` FLOAT NOT NULL,
  `games_console` FLOAT NOT NULL,
  `washer` FLOAT NOT NULL,
  `dryer` FLOAT NOT NULL,
  `dishwasher` FLOAT NOT NULL,
  `kettle` FLOAT NOT NULL,
  `other` FLOAT NOT NULL,
  `user` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`log_number`),
  INDEX `user_idx` (`user` ASC) VISIBLE,
  CONSTRAINT `user_emission`
    FOREIGN KEY (`user`)
    REFERENCES `carbonemissionscalculator`.`user_details` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 42
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`car_emissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`car_emissions` (
  `LogNumber` INT NOT NULL AUTO_INCREMENT,
  `User` VARCHAR(20) NOT NULL,
  `Date` DATE NOT NULL,
  `Vehicle` VARCHAR(10) NOT NULL,
  `value` FLOAT NOT NULL,
  PRIMARY KEY (`LogNumber`),
  INDEX `user_idx` (`User` ASC) VISIBLE,
  CONSTRAINT `username`
    FOREIGN KEY (`User`)
    REFERENCES `carbonemissionscalculator`.`user_details` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 56
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`daily_averages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`daily_averages` (
  `log_number` INT NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(20) NOT NULL,
  `oven` FLOAT NOT NULL,
  `oven_type` VARCHAR(20) NOT NULL,
  `bulb_type` VARCHAR(20) NOT NULL,
  `rooms` INT NOT NULL,
  `hours_lit` INT NOT NULL,
  `fridge_size` VARCHAR(40) NOT NULL,
  `heating_hours` FLOAT NOT NULL,
  `number_phones` INT NOT NULL,
  `pc_hours` FLOAT NOT NULL,
  `tv_hours` FLOAT NOT NULL,
  `washer_hours` FLOAT NOT NULL,
  `dryer_hours` FLOAT NOT NULL,
  `dishwasher_hours` FLOAT NOT NULL,
  `games_console_hours` FLOAT NOT NULL,
  `kettle_uses` INT NOT NULL,
  `other_hours` FLOAT NOT NULL,
  `total_daily_emission` FLOAT NOT NULL,
  PRIMARY KEY (`log_number`),
  UNIQUE INDEX `log_number_UNIQUE` (`log_number` ASC) VISIBLE,
  INDEX `username_idx` (`user` ASC) VISIBLE,
  CONSTRAINT `user_average`
    FOREIGN KEY (`user`)
    REFERENCES `carbonemissionscalculator`.`user_details` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`vehicle_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`vehicle_details` (
  `vehicle_id` INT NOT NULL AUTO_INCREMENT,
  `registration_number` VARCHAR(10) NOT NULL,
  `make` VARCHAR(20) NOT NULL,
  `model` VARCHAR(20) NOT NULL,
  `type` VARCHAR(25) NOT NULL,
  `petrol_type` VARCHAR(10) NOT NULL,
  `mpg` FLOAT NULL DEFAULT NULL,
  `owner` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE INDEX `vehicle_id_UNIQUE` (`vehicle_id` ASC) VISIBLE,
  UNIQUE INDEX `registration_number_UNIQUE` (`registration_number` ASC) VISIBLE,
  INDEX `owner_idx` (`owner` ASC) VISIBLE,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner`)
    REFERENCES `carbonemissionscalculator`.`user_details` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 26
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `carbonemissionscalculator`.`drive_averages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carbonemissionscalculator`.`drive_averages` (
  `drive_number` INT NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(20) NOT NULL,
  `vehicle_reg` VARCHAR(10) NOT NULL,
  `starting_postcode` VARCHAR(9) NOT NULL,
  `ending_postcode` VARCHAR(9) NOT NULL,
  `distance` FLOAT NOT NULL,
  `drive_emission` FLOAT NOT NULL,
  `drive_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`drive_number`),
  INDEX `user_drive_average_idx` (`user` ASC) VISIBLE,
  INDEX `vehile_reg_average_idx` (`vehicle_reg` ASC) VISIBLE,
  CONSTRAINT `user_drive_average`
    FOREIGN KEY (`user`)
    REFERENCES `carbonemissionscalculator`.`user_details` (`username`),
  CONSTRAINT `vehile_reg_average`
    FOREIGN KEY (`vehicle_reg`)
    REFERENCES `carbonemissionscalculator`.`vehicle_details` (`registration_number`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
