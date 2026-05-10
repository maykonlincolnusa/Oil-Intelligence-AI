"use client";

import { useEffect, useRef } from "react";

import { MaritimeRoute } from "@/lib/types";

type Chokepoint = {
  name: string;
  region: string;
  latitude: number;
  longitude: number;
  risk_level: string;
};

export function MaritimeMap({
  chokepoints,
  routes,
}: {
  chokepoints: Chokepoint[];
  routes: MaritimeRoute[];
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<any>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    let mounted = true;
    void (async () => {
      const maplibregl = await import("maplibre-gl");
      if (!mounted || !containerRef.current) return;

      const map = new maplibregl.Map({
        container: containerRef.current,
        style: "https://demotiles.maplibre.org/style.json",
        center: [30, 20],
        zoom: 1.8,
        attributionControl: false,
      });
      mapRef.current = map;

      map.on("load", () => {
        map.addSource("chokepoints", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: chokepoints.map((point) => ({
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [point.longitude, point.latitude],
              },
              properties: {
                name: point.name,
                risk_level: point.risk_level,
              },
            })),
          },
        });

        map.addLayer({
          id: "chokepoints-layer",
          type: "circle",
          source: "chokepoints",
          paint: {
            "circle-radius": 6,
            "circle-color": [
              "match",
              ["get", "risk_level"],
              "high",
              "#f97316",
              "medium",
              "#facc15",
              "#22c55e",
            ],
            "circle-stroke-width": 1,
            "circle-stroke-color": "#111827",
          },
        });

        map.addSource("routes", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: routes
              .filter((route) => route.coordinates.length > 1)
              .map((route) => ({
                type: "Feature",
                geometry: {
                  type: "LineString",
                  coordinates: route.coordinates,
                },
                properties: {
                  vessel_name: route.vessel_name,
                  risk: route.route_risk_score,
                },
              })),
          },
        });

        map.addLayer({
          id: "routes-layer",
          type: "line",
          source: "routes",
          paint: {
            "line-color": [
              "interpolate",
              ["linear"],
              ["get", "risk"],
              40,
              "#38bdf8",
              70,
              "#f59e0b",
              90,
              "#ef4444",
            ],
            "line-width": 2.4,
            "line-opacity": 0.85,
          },
        });
      });
    })();

    return () => {
      mounted = false;
      const map = mapRef.current;
      if (map) {
        map.remove();
      }
      mapRef.current = null;
    };
  }, [chokepoints, routes]);

  return <div ref={containerRef} className="h-[520px] w-full rounded-xl border border-slate-700" />;
}
