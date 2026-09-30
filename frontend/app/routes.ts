import { type RouteConfig, index, layout, route } from "@react-router/dev/routes";

export default [
  layout("routes/marketing-layout.tsx", [
    index("routes/home.tsx"),
    route("services", "routes/services.tsx"),
    route("partners", "routes/partners.tsx"),
  ]),
  route("login", "routes/login.tsx"),
  route("register", "routes/register.tsx"),
] satisfies RouteConfig;
