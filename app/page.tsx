"use client";

import { useEffect, useRef } from "react";
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  ChevronRight,
  Leaf,
  Mail,
  MapPin,
  Menu,
  PackageCheck,
  Phone,
  Play,
  ShieldCheck,
  ShoppingBasket,
  Sprout,
  Tractor,
  Truck,
  Users,
  Wheat
} from "lucide-react";
import { AnimatePresence, motion, useScroll, useTransform } from "framer-motion";
import Lenis from "@studio-freight/lenis";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

type IconComponent = typeof Leaf;

const farmVideo =
  "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-a-large-crop-field-45518-large.mp4";

const fadeUp = {
  hidden: { opacity: 0, y: 34 },
  show: { opacity: 1, y: 0 }
};

const trustCards = [
  {
    icon: Sprout,
    title: "Sustainable Agriculture",
    text: "Traceable sourcing, lower wastage, and smarter demand planning for every harvest."
  },
  {
    icon: Truck,
    title: "Faster Market Access",
    text: "Digital crop discovery and coordinated logistics move produce from farms to buyers faster."
  },
  {
    icon: BarChart3,
    title: "Better Farmer Income",
    text: "Transparent pricing and wider buyer access help farmers capture more value."
  }
];

const stats = [
  ["10,000+", "Farmers Connected"],
  ["50+", "Cities Served"],
  ["100,000+", "Orders Processed"]
];

const steps = [
  ["Farmer Registers", "Simple onboarding, crop profile, verification, and support."],
  ["Crop Listing", "Farmers list harvest quantity, grade, location, and availability."],
  ["Buyer Connects", "Restaurants, retailers, exporters, and buyers discover fresh supply."],
  ["Delivery & Tracking", "Logistics, quality checks, and shipment visibility complete the loop."]
];

const features: [string, IconComponent, string][] = [
  ["Smart Marketplace", ShoppingBasket, "Verified produce listings matched to live buyer demand."],
  ["Real-Time Pricing", BarChart3, "Market-aware pricing signals for fairer, faster transactions."],
  ["Crop Analytics", Wheat, "Data-driven recommendations for planning, yield, and demand."],
  ["Logistics Management", Truck, "Coordinated pickup, delivery, tracking, and route intelligence."],
  ["Buyer-Seller Network", Users, "A trusted digital network for recurring supply relationships."],
  ["Quality Assurance", ShieldCheck, "Grade standards, inspection workflows, and transparent records."]
];

const services = ["For Farmers", "For Buyers", "For Retailers", "For Restaurants", "For Exporters"];

const impacts: [string, string][] = [
  ["24,000+", "Farmers Empowered"],
  ["18,500", "Tons of Produce Delivered"],
  ["82", "Cities Connected"],
  ["1,200+", "Partner Businesses"]
];

const testimonials: [string, string, string][] = [
  ["Meera Patel", "Vegetable Farmer", "Agripick helped us sell directly to reliable buyers and plan harvests with confidence."],
  ["Arjun Rao", "Restaurant Owner", "The freshness, consistency, and delivery visibility feel built for modern food businesses."],
  ["Nisha Menon", "Retail Buyer", "We reduced procurement time and gained access to farms we could never reach before."],
  ["Kabir Singh", "Exporter", "Quality documents, tracking, and transparent sourcing made our procurement far smoother."]
];

const gallery: [string, string][] = [
  ["https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80", "Farm fields"],
  ["https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=900&q=80", "Fresh harvest"],
  ["https://images.unsplash.com/photo-1595278069441-2cf29f8005a4?auto=format&fit=crop&w=900&q=80", "Farmer with produce"],
  ["https://images.unsplash.com/photo-1530507629858-e4977d30e9e0?auto=format&fit=crop&w=900&q=80", "Greenhouse"],
  ["https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=900&q=80", "Vegetable market"],
  ["https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?auto=format&fit=crop&w=900&q=80", "Supply field"]
];

const blogPosts: [string, string][] = [
  ["Agriculture Technology", "How connected farm data is reshaping fresh produce supply chains."],
  ["Farmer Success Stories", "The new rural entrepreneurs growing income with digital market access."],
  ["Market Insights", "What buyers need to know about freshness, seasonality, and pricing."],
  ["Sustainable Farming", "Reducing waste from harvest planning to last-mile delivery."]
];

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <motion.p
      className="mb-4 inline-flex rounded-full border border-leaf/15 bg-white/70 px-4 py-2 text-sm font-semibold text-leaf shadow-sm backdrop-blur"
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-80px" }}
      variants={fadeUp}
      transition={{ duration: 0.55 }}
    >
      {children}
    </motion.p>
  );
}

function MagneticButton({
  children,
  variant = "primary"
}: {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}) {
  return (
    <motion.a
      href={variant === "primary" ? "#platform" : "#contact"}
      className={`group inline-flex items-center gap-3 rounded-full px-6 py-4 text-sm font-bold transition ${
        variant === "primary"
          ? "bg-white text-leaf shadow-2xl shadow-black/20 hover:bg-limewash"
          : "border border-white/35 bg-white/10 text-white backdrop-blur hover:bg-white/20"
      }`}
      whileHover={{ y: -3, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
      <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
    </motion.a>
  );
}

function Counter({ value }: { value: string }) {
  const counterRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const element = counterRef.current;
    if (!element) return;

    const numericValue = Number(value.replace(/\D/g, ""));
    const suffix = value.replace(/[0-9,]/g, "");
    const tween = gsap.fromTo(
      element,
      { innerText: 0 },
      {
        innerText: numericValue,
        duration: 2,
        ease: "power3.out",
        snap: { innerText: 1 },
        scrollTrigger: {
          trigger: element,
          start: "top 88%",
          once: true
        },
        onUpdate: () => {
          element.innerText = `${Number(element.innerText).toLocaleString()}${suffix}`;
        }
      }
    );

    return () => {
      tween.kill();
    };
  }, [value]);

  return <span ref={counterRef}>0</span>;
}

export default function Home() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"]
  });
  const heroTextY = useTransform(scrollYProgress, [0, 1], [0, 170]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.72], [1, 0]);

  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.18,
      smoothWheel: true,
      wheelMultiplier: 0.85
    });

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    const frame = requestAnimationFrame(raf);

    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>("[data-reveal]").forEach((element) => {
        gsap.fromTo(
          element,
          { opacity: 0, y: 42 },
          {
            opacity: 1,
            y: 0,
            duration: 0.85,
            ease: "power3.out",
            scrollTrigger: {
              trigger: element,
              start: "top 84%"
            }
          }
        );
      });

      gsap.to("[data-float]", {
        y: -24,
        rotation: 5,
        duration: 3.8,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1,
        stagger: 0.32
      });
    });

    return () => {
      cancelAnimationFrame(frame);
      lenis.destroy();
      ctx.revert();
    };
  }, []);

  return (
    <main className="relative overflow-hidden bg-cream text-slate-950">
      <AnimatePresence>
        <motion.div
          className="fixed inset-0 z-[90] grid place-items-center bg-[#04120c]"
          initial={{ opacity: 1 }}
          animate={{ opacity: 0, pointerEvents: "none" }}
          transition={{ delay: 1.05, duration: 0.7 }}
        >
          <motion.div
            className="flex items-center gap-3 rounded-full border border-white/10 px-5 py-3 text-white"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <Leaf className="h-5 w-5 text-meadow" />
            <span className="text-sm font-semibold tracking-[0.28em]">AGRIPICK</span>
          </motion.div>
        </motion.div>
      </AnimatePresence>

      <header className="fixed left-0 right-0 top-0 z-50 px-4 py-4">
        <nav className="mx-auto flex max-w-7xl items-center justify-between rounded-full border border-white/25 bg-white/70 px-5 py-3 shadow-xl shadow-leaf/10 backdrop-blur-2xl">
          <a href="#" className="flex items-center gap-3 font-black tracking-tight text-leaf">
            <span className="grid h-10 w-10 place-items-center rounded-full bg-leaf text-white shadow-glow">
              <Leaf className="h-5 w-5" />
            </span>
            Agripick
          </a>
          <div className="hidden items-center gap-7 text-sm font-semibold text-slate-700 md:flex">
            {["About", "Platform", "Services", "Blog", "Contact"].map((item) => (
              <a key={item} href={`#${item.toLowerCase()}`} className="transition hover:text-leaf">
                {item}
              </a>
            ))}
          </div>
          <a
            href="#contact"
            className="hidden rounded-full bg-leaf px-5 py-3 text-sm font-bold text-white shadow-lg shadow-leaf/25 transition hover:bg-[#0b5730] md:inline-flex"
          >
            Partner With Us
          </a>
          <button className="grid h-10 w-10 place-items-center rounded-full bg-leaf text-white md:hidden" aria-label="Open menu">
            <Menu className="h-5 w-5" />
          </button>
        </nav>
      </header>

      <section ref={heroRef} className="grain relative min-h-screen overflow-hidden bg-[#06170f] text-white">
        <video
          className="absolute inset-0 h-full w-full scale-105 object-cover opacity-70"
          src={farmVideo}
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          poster="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1800&q=80"
        />
        <div className="absolute inset-0 bg-[linear-gradient(110deg,rgba(2,16,10,0.88),rgba(4,48,27,0.48),rgba(0,0,0,0.58))]" />
        <div className="absolute inset-0 bg-hero-radial opacity-80" />

        {[...Array(18)].map((_, index) => (
          <motion.span
            key={index}
            className="absolute z-10 h-1.5 w-1.5 rounded-full bg-limewash/70"
            style={{
              left: `${8 + ((index * 19) % 86)}%`,
              top: `${12 + ((index * 13) % 74)}%`
            }}
            animate={{
              y: [0, -22, 0],
              opacity: [0.28, 0.9, 0.28],
              scale: [1, 1.7, 1]
            }}
            transition={{ duration: 4 + (index % 4), repeat: Infinity, delay: index * 0.14 }}
          />
        ))}

        <motion.div
          className="relative z-20 mx-auto flex min-h-screen max-w-7xl flex-col justify-end px-5 pb-20 pt-36 md:pb-28"
          style={{ y: heroTextY, opacity: heroOpacity }}
        >
          <motion.div
            className="max-w-5xl"
            initial={{ opacity: 0, y: 60 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut", delay: 0.25 }}
          >
            <p className="mb-5 inline-flex rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm font-semibold text-limewash backdrop-blur">
              Farm-to-market intelligence for a transparent food economy
            </p>
            <h1 className="text-balance text-5xl font-black tracking-[-0.06em] sm:text-7xl lg:text-8xl">
              Connecting Farms. Empowering Growth.
            </h1>
            <p className="mt-7 max-w-3xl text-lg leading-8 text-white/82 md:text-2xl md:leading-10">
              Agripick helps farmers, buyers, and businesses build a smarter agricultural ecosystem through technology and transparency.
            </p>
            <div className="mt-9 flex flex-col gap-4 sm:flex-row">
              <MagneticButton>Explore Platform</MagneticButton>
              <MagneticButton variant="secondary">Contact Us</MagneticButton>
            </div>
          </motion.div>
        </motion.div>

        <motion.div
          data-float
          className="absolute bottom-12 right-5 z-20 hidden rounded-[2rem] border border-white/20 bg-white/10 p-4 text-white backdrop-blur-xl md:block"
        >
          <div className="flex items-center gap-4">
            <div className="grid h-14 w-14 place-items-center rounded-2xl bg-limewash text-leaf">
              <PackageCheck className="h-7 w-7" />
            </div>
            <div>
              <p className="text-sm text-white/70">Live supply visibility</p>
              <p className="text-2xl font-black">98.4%</p>
            </div>
          </div>
        </motion.div>
      </section>

      <section id="platform" className="relative px-5 py-24 md:py-32">
        <div className="absolute left-0 top-16 h-72 w-72 rounded-full bg-meadow/20 blur-3xl" />
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Trusted AgriTech Platform</SectionLabel>
          <div className="grid gap-6 md:grid-cols-3">
            {trustCards.map(({ icon: Icon, title, text }, index) => (
              <motion.article
                key={title}
                className="glass-card group rounded-[2rem] p-8 transition hover:-translate-y-2 hover:shadow-premium"
                initial={{ opacity: 0, y: 50, rotateX: 12 }}
                whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
                viewport={{ once: true, margin: "-80px" }}
                transition={{ duration: 0.7, delay: index * 0.12 }}
                whileHover={{ rotateX: 4, rotateY: -5 }}
              >
                <div className="mb-8 grid h-16 w-16 place-items-center rounded-3xl bg-leaf text-white shadow-glow">
                  <Icon className="h-8 w-8" />
                </div>
                <h3 className="text-2xl font-black tracking-tight">{title}</h3>
                <p className="mt-4 leading-7 text-slate-600">{text}</p>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      <section id="about" className="px-5 py-24">
        <div className="mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-2">
          <div className="relative min-h-[520px]" data-reveal>
            <motion.img
              data-float
              src="https://images.unsplash.com/photo-1595278069441-2cf29f8005a4?auto=format&fit=crop&w=900&q=80"
              alt="Farmer holding fresh produce"
              className="absolute left-0 top-8 h-72 w-64 rounded-[2.5rem] object-cover shadow-premium md:h-96 md:w-80"
            />
            <motion.img
              data-float
              src="https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=900&q=80"
              alt="Fresh vegetables harvest"
              className="absolute right-0 top-0 h-60 w-56 rounded-[2rem] object-cover shadow-2xl md:h-80 md:w-72"
            />
            <motion.div
              data-float
              className="dark-glass absolute bottom-6 left-12 max-w-xs rounded-[2rem] p-6 text-white"
            >
              <Tractor className="mb-5 h-8 w-8 text-limewash" />
              <p className="text-xl font-black">Procurement, logistics, and intelligence in one operating layer.</p>
            </motion.div>
          </div>
          <div data-reveal>
            <SectionLabel>About Agripick</SectionLabel>
            <h2 className="text-balance text-4xl font-black tracking-[-0.04em] text-slate-950 md:text-6xl">
              Transforming Agriculture Through Innovation
            </h2>
            <p className="mt-6 text-lg leading-8 text-slate-600">
              Agripick bridges the gap between farmers and markets using technology, data, and transparency. Our platform creates cleaner supply chains, unlocks better market access, and gives food businesses the confidence to source directly from verified farms.
            </p>
            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              {stats.map(([number, label]) => (
                <div key={label} className="rounded-[1.5rem] border border-leaf/10 bg-white p-5 shadow-lg shadow-leaf/5">
                  <p className="text-3xl font-black text-leaf">{number}</p>
                  <p className="mt-2 text-sm font-semibold text-slate-500">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="bg-white px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>How It Works</SectionLabel>
          <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
            <h2 className="text-balance text-4xl font-black tracking-[-0.04em] md:text-6xl">
              A smarter route from harvest to happy buyers.
            </h2>
            <div className="relative">
              <div className="absolute left-7 top-8 hidden h-[calc(100%-4rem)] w-px bg-gradient-to-b from-leaf via-meadow to-transparent md:block" />
              {steps.map(([title, text], index) => (
                <motion.div
                  key={title}
                  className="relative mb-5 rounded-[2rem] border border-leaf/10 bg-cream p-6 shadow-lg shadow-leaf/5 md:ml-20"
                  initial={{ opacity: 0, x: 60 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <span className="absolute -left-20 top-6 hidden h-14 w-14 place-items-center rounded-full bg-leaf text-xl font-black text-white shadow-glow md:grid">
                    {index + 1}
                  </span>
                  <h3 className="text-2xl font-black">{title}</h3>
                  <p className="mt-2 leading-7 text-slate-600">{text}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Platform Features</SectionLabel>
          <div className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <h2 className="max-w-3xl text-4xl font-black tracking-[-0.04em] md:text-6xl">
              Built for the rhythm of modern agriculture.
            </h2>
            <p className="max-w-md text-lg leading-8 text-slate-600">
              Premium tools that make farm supply discoverable, predictable, traceable, and profitable.
            </p>
          </div>
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {features.map(([title, FeatureIcon, text]) => {
              return (
                <motion.article
                  key={title as string}
                  className="group rounded-[2rem] border border-leaf/10 bg-white p-7 shadow-lg shadow-leaf/5 transition hover:bg-leaf hover:text-white hover:shadow-glow"
                  whileHover={{ y: -8 }}
                  data-reveal
                >
                  <FeatureIcon className="mb-8 h-9 w-9 text-meadow transition group-hover:text-limewash" />
                  <h3 className="text-2xl font-black">{title}</h3>
                  <p className="mt-4 leading-7 text-slate-600 transition group-hover:text-white/78">{text}</p>
                </motion.article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="relative min-h-[760px] overflow-hidden bg-[#06170f] px-5 py-24 text-white">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_10%,rgba(46,184,114,0.35),transparent_35%)]" />
        <div className="mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-2">
          <div data-reveal>
            <p className="mb-4 text-sm font-bold uppercase tracking-[0.35em] text-limewash">Video Story</p>
            <h2 className="text-balance text-5xl font-black tracking-[-0.05em] md:text-7xl">From Farm to Future</h2>
            <p className="mt-6 text-lg leading-8 text-white/72">
              See how Agripick turns fields, transport, quality checks, and buyer demand into one transparent journey.
            </p>
          </div>
          <motion.div
            className="group relative overflow-hidden rounded-[2.5rem] border border-white/15 shadow-2xl"
            whileInView={{ scale: [0.96, 1], opacity: [0, 1] }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <video
              className="aspect-video w-full object-cover"
              src={farmVideo}
              muted
              loop
              playsInline
              preload="metadata"
              poster="https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?auto=format&fit=crop&w=1200&q=80"
            />
            <button className="absolute inset-0 grid place-items-center bg-black/20 transition group-hover:bg-black/5" aria-label="Play farm story video">
              <span className="grid h-24 w-24 place-items-center rounded-full bg-white text-leaf shadow-glow">
                <Play className="ml-1 h-9 w-9 fill-current" />
              </span>
            </button>
          </motion.div>
        </div>
      </section>

      <section id="services" className="px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Services</SectionLabel>
          <div className="grid gap-5 md:grid-cols-5">
            {services.map((service, index) => (
              <motion.article
                key={service}
                className="group min-h-80 overflow-hidden rounded-[2rem] bg-white p-6 shadow-lg shadow-leaf/5 transition-all duration-500 hover:md:col-span-2"
                whileHover={{ y: -8 }}
              >
                <div className="flex h-full flex-col justify-between">
                  <div>
                    <span className="grid h-12 w-12 place-items-center rounded-2xl bg-limewash text-leaf">
                      <ChevronRight className="h-6 w-6" />
                    </span>
                    <h3 className="mt-8 text-2xl font-black">{service}</h3>
                  </div>
                  <p className="translate-y-4 opacity-0 transition duration-500 group-hover:translate-y-0 group-hover:opacity-100">
                    Tailored sourcing, listings, quality, logistics, and relationship tools for every agricultural stakeholder.
                  </p>
                </div>
                <p className="mt-6 text-sm font-bold text-leaf">0{index + 1}</p>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Impact</SectionLabel>
          <div className="grid gap-5 md:grid-cols-4">
            {impacts.map(([value, label]) => (
              <div key={label} className="rounded-[2rem] bg-gradient-to-br from-leaf to-meadow p-7 text-white shadow-glow" data-reveal>
                <p className="text-4xl font-black md:text-5xl">
                  <Counter value={value} />
                </p>
                <p className="mt-3 font-semibold text-white/80">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="overflow-hidden px-5 py-24">
        <div className="mx-auto mb-12 max-w-7xl">
          <SectionLabel>Testimonials</SectionLabel>
          <h2 className="text-4xl font-black tracking-[-0.04em] md:text-6xl">Trusted across the fresh food chain.</h2>
        </div>
        <div className="flex w-max gap-5 marquee-track">
          {[...testimonials, ...testimonials].map(([name, role, quote], index) => (
            <article key={`${name}-${index}`} className="glass-card w-[340px] rounded-[2rem] p-6">
              <div className="mb-6 flex items-center gap-4">
                <img
                  src={`https://images.unsplash.com/photo-${index % 2 === 0 ? "1494790108377-be9c29b29330" : "1500648767791-00dcc994a43e"}?auto=format&fit=crop&w=180&q=80`}
                  alt={`${name} profile`}
                  className="h-14 w-14 rounded-full object-cover"
                />
                <div>
                  <h3 className="font-black">{name}</h3>
                  <p className="text-sm text-slate-500">{role}</p>
                </div>
              </div>
              <p className="leading-7 text-slate-600">“{quote}”</p>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-white px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Gallery</SectionLabel>
          <div className="masonry">
            {gallery.map(([src, alt], index) => (
              <motion.div key={src} className="group overflow-hidden rounded-[2rem]" whileHover={{ scale: 0.98 }}>
                <img
                  src={src}
                  alt={alt}
                  className={`w-full object-cover transition duration-700 group-hover:scale-110 ${index % 2 ? "h-72" : "h-96"}`}
                  loading="lazy"
                />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative overflow-hidden bg-[#06170f] px-5 py-24 text-white">
        <div className="absolute -right-24 top-10 h-96 w-96 rounded-full bg-meadow/30 blur-3xl" />
        <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-2">
          <div data-reveal>
            <p className="mb-4 text-sm font-bold uppercase tracking-[0.35em] text-limewash">Partner / B2B</p>
            <h2 className="text-5xl font-black tracking-[-0.05em] md:text-7xl">Grow With Agripick</h2>
            <p className="mt-6 max-w-xl text-lg leading-8 text-white/72">
              Restaurants, retail chains, food businesses, and export companies use Agripick to source dependable produce at scale.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              {["Restaurants", "Retail Chains", "Food Businesses", "Export Companies"].map((item) => (
                <span key={item} className="rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-semibold backdrop-blur">
                  {item}
                </span>
              ))}
            </div>
          </div>
          <form className="dark-glass rounded-[2rem] p-6" data-reveal>
            <div className="grid gap-4 sm:grid-cols-2">
              <input className="rounded-2xl border border-white/10 bg-white/10 px-4 py-4 outline-none placeholder:text-white/45" placeholder="Name" />
              <input className="rounded-2xl border border-white/10 bg-white/10 px-4 py-4 outline-none placeholder:text-white/45" placeholder="Company" />
              <input className="rounded-2xl border border-white/10 bg-white/10 px-4 py-4 outline-none placeholder:text-white/45 sm:col-span-2" placeholder="Email" />
              <textarea className="min-h-32 rounded-2xl border border-white/10 bg-white/10 px-4 py-4 outline-none placeholder:text-white/45 sm:col-span-2" placeholder="Tell us what you source" />
            </div>
            <button className="mt-5 inline-flex rounded-full bg-limewash px-6 py-4 font-black text-leaf transition hover:bg-white" type="button">
              Send Inquiry
            </button>
          </form>
        </div>
      </section>

      <section id="blog" className="px-5 py-24">
        <div className="mx-auto max-w-7xl">
          <SectionLabel>Blog</SectionLabel>
          <div className="grid gap-5 md:grid-cols-4">
            {blogPosts.map(([title, text]) => (
              <article key={title} className="rounded-[2rem] border border-leaf/10 bg-white p-6 shadow-lg shadow-leaf/5 transition hover:-translate-y-2 hover:shadow-premium">
                <p className="mb-10 text-sm font-black uppercase tracking-[0.22em] text-meadow">Insights</p>
                <h3 className="text-2xl font-black">{title}</h3>
                <p className="mt-4 leading-7 text-slate-600">{text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="contact" className="bg-white px-5 py-24">
        <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <SectionLabel>Contact</SectionLabel>
            <h2 className="text-4xl font-black tracking-[-0.04em] md:text-6xl">Let’s build the next food supply layer.</h2>
            <div className="mt-8 space-y-4">
              <a href="mailto:hello@agripick.com" className="flex items-center gap-3 font-bold text-leaf">
                <Mail className="h-5 w-5" /> hello@agripick.com
              </a>
              <a href="https://wa.me/919999999999" className="flex items-center gap-3 font-bold text-leaf">
                <Phone className="h-5 w-5" /> WhatsApp Agripick
              </a>
              <p className="flex items-center gap-3 font-bold text-slate-700">
                <MapPin className="h-5 w-5 text-leaf" /> Bengaluru, India
              </p>
            </div>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            <form className="rounded-[2rem] bg-cream p-6 shadow-lg shadow-leaf/5">
              <input className="mb-4 w-full rounded-2xl border border-leaf/10 bg-white px-4 py-4 outline-none focus:border-leaf" placeholder="Full name" />
              <input className="mb-4 w-full rounded-2xl border border-leaf/10 bg-white px-4 py-4 outline-none focus:border-leaf" placeholder="Email address" />
              <textarea className="mb-4 min-h-32 w-full rounded-2xl border border-leaf/10 bg-white px-4 py-4 outline-none focus:border-leaf" placeholder="Message" />
              <button type="button" className="w-full rounded-full bg-leaf px-6 py-4 font-black text-white transition hover:bg-[#0b5730]">
                Contact Us
              </button>
            </form>
            <iframe
              title="Agripick map"
              className="min-h-[420px] w-full rounded-[2rem] border-0 shadow-lg shadow-leaf/5"
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              src="https://www.google.com/maps?q=Bengaluru%20India&output=embed"
            />
          </div>
        </div>
      </section>

      <footer className="bg-[#04120c] px-5 py-14 text-white">
        <div className="mx-auto grid max-w-7xl gap-10 md:grid-cols-[1.2fr_0.8fr_1fr]">
          <div>
            <a href="#" className="flex items-center gap-3 text-2xl font-black">
              <span className="grid h-12 w-12 place-items-center rounded-full bg-limewash text-leaf">
                <Leaf className="h-6 w-6" />
              </span>
              Agripick
            </a>
            <p className="mt-5 max-w-md leading-7 text-white/60">
              Connecting farms, empowering growth, and making fresh supply chains more transparent.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4 text-white/70">
            {["Home", "About", "Services", "Blog", "Contact"].map((link) => (
              <a key={link} href={link === "Home" ? "#" : `#${link.toLowerCase()}`} className="hover:text-white">
                {link}
              </a>
            ))}
          </div>
          <div>
            <p className="font-black">Join the harvest letter</p>
            <div className="mt-4 flex rounded-full border border-white/10 bg-white/10 p-1">
              <input className="min-w-0 flex-1 bg-transparent px-4 outline-none placeholder:text-white/35" placeholder="Email" />
              <button className="rounded-full bg-limewash px-5 py-3 font-black text-leaf">Subscribe</button>
            </div>
            <div className="mt-5 flex gap-3 text-sm font-bold text-white/60">
              <a href="#">LinkedIn</a>
              <a href="#">Instagram</a>
              <a href="#">X</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
