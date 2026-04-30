import { createRouter as createTanStackRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import type { QueryClient } from "@tanstack/react-query";

export function createRouter(queryClient: QueryClient) {
    const router = createTanStackRouter({
        routeTree,
        context: {
            queryClient,
        },
        scrollRestoration: true,
        defaultPreloadStaleTime: 0,
    });

    return router;
}

declare module "@tanstack/react-router" {
    interface Register {
        router: ReturnType<typeof createRouter>;
    }
}
