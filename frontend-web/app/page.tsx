"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type Service = {
  id: number;
  service_type: string;
  title: string;
  description?: string;
  city?: string;
  country?: string;
  price_estimated?: number;
  currency?: string;
  source: string;
};

export default function Home() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const res = await api.get("/services");
      setServices(res.data);
    } catch {
      alert("فشل تحميل الخدمات المتاحة");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <main style={{ padding: 40 }}>
      <h1>ALFA — منصة السفر والخدمات المحلية</h1>
      <p style={{ color: "#555", marginBottom: 20 }}>
        ابحث عن الرحلات، الفنادق، السيارات، التوصيل، السياحة، الحج والعمرة،
        وكل الخدمات المحلية — والتنفيذ يتم عبر وكلائنا المعتمدين.
      </p>

      {loading && <p>جاري تحميل الخدمات…</p>}

      {!loading && services.length === 0 && (
        <p>لا تو
