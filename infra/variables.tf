# General Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "serverless-secure-webapp"
}

# VPC Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

# Database Variables
variable "db_engine" {
  description = "Database engine"
  type        = string
  default     = "mysql"
  validation {
    condition     = contains(["mysql", "postgres"], var.db_engine)
    error_message = "Database engine must be either 'mysql' or 'postgres'."
  }
}

variable "db_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "8.0"
}

variable "db_instance_class" {
  description = "Database instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Initial allocated storage for database (GB)"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for database (GB)"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "webapp"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "admin"
}

variable "db_port" {
  description = "Database port"
  type        = number
  default     = 3306
}

variable "db_backup_retention_period" {
  description = "Database backup retention period (days)"
  type        = number
  default     = 7
}

variable "db_backup_window" {
  description = "Database backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "db_maintenance_window" {
  description = "Database maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "db_skip_final_snapshot" {
  description = "Skip final snapshot when destroying database"
  type        = bool
  default     = true
}

variable "db_deletion_protection" {
  description = "Enable deletion protection for database"
  type        = bool
  default     = false
}

# Environment Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# Tags
variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "serverless-secure-webapp"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}
