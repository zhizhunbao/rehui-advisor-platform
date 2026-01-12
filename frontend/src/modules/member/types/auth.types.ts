export interface LoginDto {
  email: string;
  password: string;
}

export interface RegisterDto {
  email: string;
  password: string;
  name?: string;
}

export interface UpdatePasswordDto {
  oldPassword: string;
  newPassword: string;
}

export type UserType = "ANONYMOUS" | "REGISTERED" | "PREMIUM";

export interface User {
  id: string;
  email: string | null;
  name: string | null;
  userType: UserType;
  isAnonymous?: boolean;
}

export interface QuotaStatus {
  userType: UserType;
  searchCount: number;
  searchLimit: number;
  remaining: number;
  resetAt: string | null;
  canSearch: boolean;
  message?: string;
}
