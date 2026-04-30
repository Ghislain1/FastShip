import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background">
      <h1 className="text-4xl font-bold text-foreground">FastShip</h1>
      <p className="mt-4 text-lg text-muted-foreground">
        Shipping & E-commerce Platform
      </p>
    </div>
  );
}
