import {
  Plane,
  Hotel,
  Briefcase,
  Car,
  Home,
  ShieldCheck,
  GraduationCap,
  TrendingUp,
} from "lucide-react";

export const getIcon = (name: string, className?: string) => {
  switch (name) {
    case "Plane":
      return <Plane className={className} />;
    case "Hotel":
      return <Hotel className={className} />;
    case "Briefcase":
      return <Briefcase className={className} />;
    case "Car":
      return <Car className={className} />;
    case "Home":
      return <Home className={className} />;
    case "ShieldCheck":
      return <ShieldCheck className={className} />;
    case "GraduationCap":
      return <GraduationCap className={className} />;
    case "TrendingUp":
      return <TrendingUp className={className} />;
    default:
      return <Plane className={className} />;
  }
};
