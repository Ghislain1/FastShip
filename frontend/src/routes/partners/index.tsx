import { createFileRoute } from "@tanstack/react-router";
import PartnersPage from "~/pages/services/PartnersPage";

export const Route = createFileRoute("/partners/")({
    component: PartnersPage,
});
