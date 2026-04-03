import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  TrendingUp, 
  Home, 
  Building2, 
  MapPin, 
  Calculator, 
  ChevronRight, 
  ArrowUpRight, 
  Info,
  Layers,
  Search,
  Check,
  Zap
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  ScatterChart, 
  Scatter, 
  ZAxis,
  Cell,
  Legend,
  PieChart,
  Pie
} from 'recharts';
import { cn } from './lib/utils';

// --- Mock Data ---

const REGIONS = ['Flanders', 'Wallonia', 'Brussels'];
const PROVINCES_BY_REGION: Record<string, string[]> = {
  'Flanders': ['Antwerp', 'East Flanders', 'Flemish Brabant', 'Limburg', 'West Flanders'],
  'Wallonia': ['Hainaut', 'Liège', 'Luxembourg', 'Namur', 'Walloon Brabant'],
  'Brussels': ['Brussels']
};
const PROPERTY_TYPES = ['House', 'Apartment'];
const SUBTYPES_BY_TYPE: Record<string, string[]> = {
  'House': ['residence', 'villa', 'mixed-building', 'master-house', 'cottage', 'bungalow', 'chalet', 'mansion'],
  'Apartment': ['apartment', 'penthouse', 'ground-floor', 'duplex', 'studio', 'loft', 'triplex']
};
const TYPES_OF_SALE = ['for sale', 'in public sale'];
const KITCHEN_TYPES = ['Not equipped', 'Partially equipped', 'Super equipped', 'Fully equipped'];
const BUILDING_STATES = [
  'New', 'Under construction', 'Fully renovated', 'Excellent', 
  'Normal', 'To be renovated', 'To renovate', 'To restore', 'To demolish'
];

const regionalData = [
  { name: 'Brussels', house: 485000, apartment: 312000, avgM2: 3200 },
  { name: 'Flanders', house: 340000, apartment: 245000, avgM2: 2600 },
  { name: 'Wallonia', house: 210000, apartment: 185000, avgM2: 1800 },
];

const scatterData = [
  { area: 80, price: 250000, region: 'Flanders' },
  { area: 120, price: 380000, region: 'Flanders' },
  { area: 150, price: 450000, region: 'Flanders' },
  { area: 200, price: 580000, region: 'Flanders' },
  { area: 60, price: 280000, region: 'Brussels' },
  { area: 90, price: 420000, region: 'Brussels' },
  { area: 130, price: 550000, region: 'Brussels' },
  { area: 180, price: 720000, region: 'Brussels' },
  { area: 100, price: 180000, region: 'Wallonia' },
  { area: 140, price: 240000, region: 'Wallonia' },
  { area: 190, price: 310000, region: 'Wallonia' },
  { area: 250, price: 420000, region: 'Wallonia' },
];

const housingClassesData = {
  House: [
    { name: 'Budget (<300k)', value: 35, color: '#E5E7EB' },
    { name: 'Mid-Range (300k-600k)', value: 45, color: '#9CA3AF' },
    { name: 'Premium (600k-1.2M)', value: 15, color: '#4B5563' },
    { name: 'Luxury (>1.2M)', value: 5, color: '#1F2937' },
  ],
  Apartment: [
    { name: 'Budget (<300k)', value: 55, color: '#E5E7EB' },
    { name: 'Mid-Range (300k-600k)', value: 35, color: '#9CA3AF' },
    { name: 'Premium (600k-1.2M)', value: 8, color: '#4B5563' },
    { name: 'Luxury (>1.2M)', value: 2, color: '#1F2937' },
  ],
};

const topExpensiveTotal = [
  { name: 'Knokke-Heist', price: '€845,000' },
  { name: 'Ixelles', price: '€720,000' },
  { name: 'Uccle', price: '€695,000' },
  { name: 'Sint-Martens-Latem', price: '€680,000' },
  { name: 'Woluwe-Saint-Pierre', price: '€650,000' },
];

const topExpensiveM2 = [
  { name: 'Ixelles', price: '€4,850/m²' },
  { name: 'Saint-Gilles', price: '€4,600/m²' },
  { name: 'Brussels City', price: '€4,400/m²' },
  { name: 'Etterbeek', price: '€4,350/m²' },
  { name: 'Knokke-Heist', price: '€4,200/m²' },
];

const topAffordableTotal = [
  { name: 'Hastière', price: '€115,000' },
  { name: 'Colfontaine', price: '€128,000' },
  { name: 'Quaregnon', price: '€132,000' },
  { name: 'Viroinval', price: '€135,000' },
  { name: 'Froidchapelle', price: '€140,000' },
];

const topAffordableM2 = [
  { name: 'Colfontaine', price: '€1,050/m²' },
  { name: 'Quaregnon', price: '€1,120/m²' },
  { name: 'Frameries', price: '€1,180/m²' },
  { name: 'Dour', price: '€1,220/m²' },
  { name: 'Charleroi', price: '€1,250/m²' },
];

// --- Components ---

const Navbar = () => (
  <nav className="fixed top-0 left-0 right-0 z-50 bg-belgi-dark/95 backdrop-blur-sm border-b border-white/10 px-6 py-5 flex items-center justify-between">
    <div className="flex items-center gap-4">
      <span className="text-3xl font-serif font-bold text-white tracking-tight">
        Belgi<span className="text-belgi-gold">Immo</span>
      </span>
      <div className="hidden lg:block h-8 w-px bg-white/10 mx-2" />
      <span className="hidden lg:block text-[10px] font-bold uppercase tracking-[0.3em] text-white/40 max-w-30 leading-tight">
        Belgium Real Estate Intelligence
      </span>
    </div>
    <div className="hidden md:flex items-center gap-8 text-sm font-medium text-white/70">
      <a href="#insights" className="hover:text-belgi-gold transition-colors">Insights</a>
      <a href="#regions" className="hover:text-belgi-gold transition-colors">Regions</a>
      <a href="#prediction" className="hover:text-belgi-gold transition-colors">Price Prediction</a>
    </div>
  </nav>
);

const MetricCard = ({ title, value, subtext, icon: Icon }: any) => (
  <motion.div 
    whileHover={{ y: -5 }}
    className="bg-white p-8 rounded-2xl border border-belgi-dark/5 shadow-sm flex flex-col gap-4"
  >
    <div className="flex justify-between items-start">
      <div className="p-3 bg-belgi-gold/10 rounded-xl">
        <Icon className="w-6 h-6 text-belgi-gold" />
      </div>
    </div>
    <div>
      <h3 className="text-belgi-dark/60 text-sm font-medium uppercase tracking-wider mb-1">{title}</h3>
      <div className="text-4xl font-serif font-bold text-belgi-dark">{value}</div>
      <p className="text-belgi-dark/40 text-sm mt-2">{subtext}</p>
    </div>
  </motion.div>
);

const DataTable = ({ title, data }: { title: string, data: any[] }) => (
  <div className="bg-white rounded-2xl border border-belgi-dark/5 shadow-sm overflow-hidden h-full">
    <div className="px-6 py-4 border-b border-belgi-dark/5 bg-belgi-bg/50">
      <h4 className="font-serif italic text-belgi-dark/80 text-sm">{title}</h4>
    </div>
    <div className="divide-y divide-belgi-dark/5">
      {data.map((item, idx) => (
        <div key={idx} className="px-6 py-4 flex justify-between items-center hover:bg-belgi-bg/30 transition-colors">
          <span className="text-sm font-medium text-belgi-dark/80">{item.name}</span>
          <span className="font-mono text-xs font-bold text-belgi-dark">{item.price}</span>
        </div>
      ))}
    </div>
  </div>
);

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    zip_code: '',
    province: '',
    region: '',
    type_of_property: '',
    subtype_of_property: '',
    type_of_sale: '',
    number_of_rooms: '',
    living_area: '',
    fully_equipped_kitchen: '',
    furnished: false,
    open_fire: false,
    terrace: false,
    terrace_area: '',
    garden: false,
    garden_area: '',
    surface_of_the_land: '',
    number_of_facades: '',
    swimming_pool: false,
    state_of_the_building: ''
  });
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Attempt to call the FastAPI backend
      const response = await fetch(`${BACKEND_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          number_of_rooms: parseInt(formData.number_of_rooms) || 0,
          living_area: parseFloat(formData.living_area) || 0,
          terrace_area: parseFloat(formData.terrace_area) || 0,
          garden_area: parseFloat(formData.garden_area) || 0,
          surface_of_the_land: parseFloat(formData.surface_of_the_land) || 0,
          number_of_facades: parseInt(formData.number_of_facades) || 0,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction);
      } else {
        throw new Error('Backend unreachable or error');
      }
    } catch (err) {
      console.warn('Backend not available, using mock logic:', err);
      // Fallback to mock calculation logic
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      let base = formData.type_of_property === 'House' ? 250000 : 180000;
      const area = parseFloat(formData.living_area) || 100;
      const multiplier = formData.region === 'Brussels' ? 4200 : formData.region === 'Flanders' ? 3200 : 2200;
      const rooms = parseInt(formData.number_of_rooms) || 1;
      
      let result = base + (area * multiplier / 10) + (rooms * 15000);
      if (formData.swimming_pool) result += 30000;
      if (formData.garden) result += 20000 + (parseFloat(formData.garden_area) || 0) * 50;
      
      setPrediction(result);
    } finally {
      setLoading(false);
    }
  };

  const handleRegionChange = (region: string) => {
    setFormData({
      ...formData, 
      region, 
      province: PROVINCES_BY_REGION[region]?.[0] || '' 
    });
  };

  const handleTypeChange = (type: string) => {
    setFormData({
      ...formData, 
      type_of_property: type, 
      subtype_of_property: SUBTYPES_BY_TYPE[type]?.[0] || '' 
    });
  };

  return (
    <div className="bg-white p-10 rounded-3xl border border-belgi-dark/5 shadow-xl max-w-5xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-12">
        {/* Location & Type */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Region</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.region}
              onChange={(e) => handleRegionChange(e.target.value)}
              required
            >
              <option value="">Select region</option>
              {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Province</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.province}
              onChange={(e) => setFormData({...formData, province: e.target.value})}
              required
              disabled={!formData.region}
            >
              <option value="">Select province</option>
              {formData.region && PROVINCES_BY_REGION[formData.region].map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Zip Code</label>
            <input 
              type="text" 
              placeholder="e.g. 1000"
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.zip_code}
              onChange={(e) => setFormData({...formData, zip_code: e.target.value})}
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Property Type</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.type_of_property}
              onChange={(e) => handleTypeChange(e.target.value)}
              required
            >
              <option value="">Select type</option>
              {PROPERTY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Subtype</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.subtype_of_property}
              onChange={(e) => setFormData({...formData, subtype_of_property: e.target.value})}
              required
              disabled={!formData.type_of_property}
            >
              <option value="">Select subtype</option>
              {formData.type_of_property && SUBTYPES_BY_TYPE[formData.type_of_property].map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Type of Sale</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.type_of_sale}
              onChange={(e) => setFormData({...formData, type_of_sale: e.target.value})}
              required
            >
              <option value="">Select sale type</option>
              {TYPES_OF_SALE.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>

        {/* Interior Details */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Rooms</label>
            <input 
              type="number" 
              placeholder="0"
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.number_of_rooms}
              onChange={(e) => setFormData({...formData, number_of_rooms: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Living Area (m²)</label>
            <input 
              type="number" 
              placeholder="0"
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.living_area}
              onChange={(e) => setFormData({...formData, living_area: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Kitchen</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.fully_equipped_kitchen}
              onChange={(e) => setFormData({...formData, fully_equipped_kitchen: e.target.value})}
              required
            >
              <option value="">Kitchen status</option>
              {KITCHEN_TYPES.map(k => <option key={k} value={k}>{k}</option>)}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Building State</label>
            <select 
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.state_of_the_building}
              onChange={(e) => setFormData({...formData, state_of_the_building: e.target.value})}
              required
            >
              <option value="">Select state</option>
              {BUILDING_STATES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>

        {/* Exterior & Land */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Land Surface (m²)</label>
            <input 
              type="number" 
              placeholder="0"
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.surface_of_the_land}
              onChange={(e) => setFormData({...formData, surface_of_the_land: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-belgi-dark/50">Facades</label>
            <input 
              type="number" 
              placeholder="0"
              className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
              value={formData.number_of_facades}
              onChange={(e) => setFormData({...formData, number_of_facades: e.target.value})}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            {formData.terrace && (
              <div className="space-y-2">
                <label className="text-[10px] font-bold uppercase tracking-widest text-belgi-dark/50">Terrace Area</label>
                <input 
                  type="number" 
                  placeholder="m²"
                  className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
                  value={formData.terrace_area}
                  onChange={(e) => setFormData({...formData, terrace_area: e.target.value})}
                />
              </div>
            )}
            {formData.garden && (
              <div className="space-y-2">
                <label className="text-[10px] font-bold uppercase tracking-widest text-belgi-dark/50">Garden Area</label>
                <input 
                  type="number" 
                  placeholder="m²"
                  className="w-full p-4 bg-belgi-bg rounded-xl border-none focus:ring-2 focus:ring-belgi-gold outline-none text-belgi-dark font-medium"
                  value={formData.garden_area}
                  onChange={(e) => setFormData({...formData, garden_area: e.target.value})}
                />
              </div>
            )}
          </div>
        </div>

        {/* Toggles */}
        <div className="flex flex-wrap items-center gap-x-12 gap-y-6 pt-4 border-t border-belgi-dark/5">
          {[
            { id: 'furnished', label: 'Furnished' },
            { id: 'open_fire', label: 'Open Fire' },
            { id: 'terrace', label: 'Terrace' },
            { id: 'garden', label: 'Garden' },
            { id: 'swimming_pool', label: 'Swimming Pool' }
          ].map((item) => (
            <label key={item.id} className="flex items-center gap-3 cursor-pointer group">
              <div className={cn(
                "w-6 h-6 rounded border-2 flex items-center justify-center transition-all",
                (formData as any)[item.id] ? "bg-belgi-gold border-belgi-gold" : "border-belgi-dark/20 group-hover:border-belgi-gold"
              )} onClick={() => setFormData({...formData, [item.id]: !(formData as any)[item.id]})}>
                {(formData as any)[item.id] && <Check className="w-4 h-4 text-white" />}
              </div>
              <span className="text-sm font-semibold text-belgi-dark/70">{item.label}</span>
            </label>
          ))}
        </div>

        <div className="pt-4">
          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-belgi-gold hover:bg-belgi-gold/90 text-belgi-dark py-5 rounded-2xl font-bold text-lg flex items-center justify-center gap-3 transition-all shadow-lg shadow-belgi-gold/20 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-belgi-dark/20 border-t-belgi-dark rounded-full animate-spin" />
            ) : (
              <>
                <Calculator className="w-6 h-6" />
                Get Price Estimate
              </>
            )}
          </button>
        </div>
      </form>

      <AnimatePresence>
        {prediction && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-12 p-8 bg-belgi-dark rounded-3xl text-center"
          >
            <div className="text-belgi-gold/60 text-xs font-bold uppercase tracking-widest mb-2">Estimated Market Value</div>
            <div className="text-5xl md:text-6xl font-serif font-bold text-white mb-4">
              €{prediction.toLocaleString()}
            </div>
            <div className="text-white/40 text-sm max-w-md mx-auto">
              This estimate is based on current market trends and similar properties in the {formData.region} area.
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function App() {
  const [activeHousingFilter, setActiveHousingFilter] = useState<'House' | 'Apartment'>('House');
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/stats`);
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        }
      } catch (err) {
        console.warn('Failed to fetch market stats:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  // Use fetched stats or fallback to mock data if API fails
  const displayStats = stats || {
    summary: { avg_price: 345000, transactions: 128000, regions_tracked: 3 },
    top_expensive: { total: topExpensiveTotal, per_m2: topExpensiveM2 },
    top_affordable: { total: topAffordableTotal, per_m2: topAffordableM2 },
    regional_comparison: regionalData,
    scatter_data: scatterData,
    market_distribution: housingClassesData
  };

  return (
    <div className="min-h-screen">
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center px-6 md:px-20 py-32 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&q=80&w=2000" 
            alt="Brussels Architecture" 
            className="w-full h-full object-cover brightness-[0.35]"
            referrerPolicy="no-referrer"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-belgi-dark via-belgi-dark/60 to-transparent" />
        </div>

        <div className="relative z-10 max-w-5xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="text-belgi-gold font-bold tracking-[0.4em] uppercase text-xs md:text-sm mb-4 block">
              Belgium Real Estate Intelligence
            </span>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-serif font-bold text-white leading-[1.1] mb-6">
              Understand the Market. <br className="hidden md:block" />
              <span className="text-belgi-gold">Predict the Price.</span>
            </h1>
            <p className="text-base md:text-lg text-white/70 max-w-xl mb-8 leading-relaxed">
              Data-driven insights and AI-powered price predictions across Belgium's three regions. Make smarter property decisions.
            </p>
            
            <div className="flex flex-wrap gap-4 md:gap-6 mb-10">
              <div className="bg-white/5 backdrop-blur-md border border-white/10 p-4 md:p-5 rounded-xl min-w-[160px]">
                <div className="text-white/40 text-[9px] font-bold uppercase tracking-widest mb-1">Avg. Price</div>
                <div className="text-xl md:text-2xl font-serif font-bold text-white">€{displayStats.summary.avg_price.toLocaleString()}</div>
              </div>
              <div className="bg-white/5 backdrop-blur-md border border-white/10 p-4 md:p-5 rounded-xl min-w-[160px]">
                <div className="text-white/40 text-[9px] font-bold uppercase tracking-widest mb-1">Transactions</div>
                <div className="text-xl md:text-2xl font-serif font-bold text-white">{displayStats.summary.transactions.toLocaleString()}</div>
              </div>
              <div className="bg-white/5 backdrop-blur-md border border-white/10 p-4 md:p-5 rounded-xl min-w-[160px]">
                <div className="text-white/40 text-[9px] font-bold uppercase tracking-widest mb-1">Regions Tracked</div>
                <div className="text-xl md:text-2xl font-serif font-bold text-white">{displayStats.summary.regions_tracked}</div>
                <div className="text-white/60 text-[10px] mt-1">Brussels • Flanders • Wallonia</div>
              </div>
            </div>

            <a 
              href="#prediction"
              className="inline-flex items-center gap-3 bg-belgi-gold hover:bg-belgi-gold/90 text-belgi-dark px-6 py-3 md:py-4 rounded-xl font-bold text-base md:text-lg transition-all group shadow-xl shadow-belgi-gold/20"
            >
              Try Price Prediction
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
          </motion.div>
        </div>
      </section>

      {/* Section 1: Key Market Insights */}
      <section id="insights" className="py-24 px-6 md:px-20 bg-belgi-bg">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            <MetricCard 
              title="Avg House Price" 
              value={`€${displayStats.summary.avg_price.toLocaleString()}`} 
              subtext="National average for 2025" 
              icon={Home} 
            />
            <MetricCard 
              title="Transactions" 
              value={displayStats.summary.transactions.toLocaleString()} 
              subtext="Total tracked volume" 
              icon={Building2} 
            />
            <MetricCard 
              title="Price Stabilization" 
              value="€3,200/m²" 
              subtext="Brussels apartment average" 
              icon={TrendingUp} 
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <DataTable title="Top 5 Most Expensive (Total)" data={displayStats.top_expensive.total} />
            <DataTable title="Top 5 Most Expensive (per m²)" data={displayStats.top_expensive.per_m2} />
            <DataTable title="Top 5 Most Affordable (Total)" data={displayStats.top_affordable.total} />
            <DataTable title="Top 5 Most Affordable (per m²)" data={displayStats.top_affordable.per_m2} />
          </div>
        </div>
      </section>

      {/* Section 2: Regional Comparison */}
      <section id="regions" className="py-24 px-6 md:px-20 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <span className="text-belgi-gold font-bold tracking-[0.3em] uppercase text-xs mb-4 block">Regional Overview</span>
            <h2 className="text-5xl md:text-6xl font-serif font-bold text-belgi-dark mb-12">Compare by Region</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
              {displayStats.regional_comparison.map((region: any) => (
                <div key={region.name} className="relative group">
                  <div className="absolute inset-0 bg-gradient-to-b from-belgi-dark/80 to-belgi-dark rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  <div className="relative p-8 rounded-3xl border border-belgi-dark/5 bg-belgi-bg/30 group-hover:bg-transparent transition-colors duration-500">
                    <h3 className="text-2xl font-serif font-bold text-belgi-dark group-hover:text-white mb-2">{region.name}</h3>
                    <div className="text-3xl font-serif font-bold text-belgi-gold mb-6">€{region.house.toLocaleString()}</div>
                    <div className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-belgi-dark/40 group-hover:text-white/40">Price/m²</span>
                        <span className="font-bold text-belgi-dark group-hover:text-white">€{region.avgM2.toLocaleString()}</span>
                      </div>
                    </div>
                    <div className="mt-8 pt-8 border-t border-belgi-dark/5 group-hover:border-white/10">
                      <div className="text-xs font-bold uppercase tracking-widest text-belgi-dark/30 group-hover:text-white/30 mb-4">Highlights</div>
                      <ul className="space-y-2">
                        {region.name === 'Brussels' && ['International demand', 'Apartment-dominant', 'EU institutions proximity'].map(h => (
                          <li key={h} className="flex items-center gap-2 text-sm text-belgi-dark/70 group-hover:text-white/70">
                            <div className="w-1.5 h-1.5 rounded-full bg-belgi-gold" /> {h}
                          </li>
                        ))}
                        {region.name === 'Flanders' && ['Strong economic base', 'Family homes preferred', 'Excellent transport links'].map(h => (
                          <li key={h} className="flex items-center gap-2 text-sm text-belgi-dark/70 group-hover:text-white/70">
                            <div className="w-1.5 h-1.5 rounded-full bg-belgi-gold" /> {h}
                          </li>
                        ))}
                        {region.name === 'Wallonia' && ['Highest growth potential', 'Affordable entry', 'Nature & quality of life'].map(h => (
                          <li key={h} className="flex items-center gap-2 text-sm text-belgi-dark/70 group-hover:text-white/70">
                            <div className="w-1.5 h-1.5 rounded-full bg-belgi-gold" /> {h}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-20">
            <div className="bg-belgi-bg/50 p-8 rounded-3xl border border-belgi-dark/5">
              <h4 className="text-xl font-serif font-bold mb-8">House vs Apartment Prices</h4>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={displayStats.regional_comparison}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fontWeight: 500 }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12 }} tickFormatter={(v) => `€${v/1000}k`} />
                    <Tooltip 
                      contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                      formatter={(v: any) => [`€${v.toLocaleString()}`, '']}
                    />
                    <Legend iconType="circle" />
                    <Bar dataKey="house" name="House" fill="#1A1C20" radius={[4, 4, 0, 0]} barSize={40} />
                    <Bar dataKey="apartment" name="Apartment" fill="#D4AF37" radius={[4, 4, 0, 0]} barSize={40} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-belgi-bg/50 p-8 rounded-3xl border border-belgi-dark/5">
              <h4 className="text-xl font-serif font-bold mb-8">Price vs Area (m²)</h4>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                    <XAxis type="number" dataKey="area" name="Area" unit="m²" axisLine={false} tickLine={false} />
                    <YAxis type="number" dataKey="price" name="Price" axisLine={false} tickLine={false} tickFormatter={(v) => `€${v/1000}k`} />
                    <ZAxis type="category" dataKey="region" name="Region" />
                    <Tooltip 
                      cursor={{ strokeDasharray: '3 3' }}
                      contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                    />
                    <Legend />
                    <Scatter name="Brussels" data={displayStats.scatter_data.filter((d: any) => d.region === 'Brussels')} fill="#1A1C20" />
                    <Scatter name="Flanders" data={displayStats.scatter_data.filter((d: any) => d.region === 'Flanders')} fill="#D4AF37" />
                    <Scatter name="Wallonia" data={displayStats.scatter_data.filter((d: any) => d.region === 'Wallonia')} fill="#F27D26" />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Housing Classes */}
      <section className="py-24 px-6 md:px-20 bg-belgi-bg">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
            <div className="max-w-2xl">
              <h2 className="text-5xl font-serif font-bold text-belgi-dark mb-6">Market Distribution</h2>
              <p className="text-belgi-dark/50">
                Visualizing the Belgian market across different price segments. Filter by property type to see how the distribution shifts.
              </p>
            </div>
            <div className="flex bg-white p-1 rounded-2xl shadow-sm border border-belgi-dark/5">
              {PROPERTY_TYPES.map((type) => (
                <button
                  key={type}
                  onClick={() => setActiveHousingFilter(type as any)}
                  className={cn(
                    "px-8 py-3 rounded-xl text-sm font-bold transition-all",
                    activeHousingFilter === type ? "bg-belgi-dark text-white shadow-lg" : "text-belgi-dark/40 hover:text-belgi-dark"
                  )}
                >
                  {type}s
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div className="h-[500px] relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={displayStats.market_distribution[activeHousingFilter]}
                    cx="50%"
                    cy="50%"
                    innerRadius={120}
                    outerRadius={180}
                    paddingAngle={8}
                    dataKey="value"
                  >
                    {displayStats.market_distribution[activeHousingFilter].map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <div className="text-belgi-dark/40 text-xs font-bold uppercase tracking-widest">Market Share</div>
                <div className="text-4xl font-serif font-bold text-belgi-dark">{activeHousingFilter}</div>
              </div>
            </div>

            <div className="space-y-8">
              {displayStats.market_distribution[activeHousingFilter].map((item: any, idx: number) => (
                <motion.div 
                  key={item.name}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="flex items-center gap-6 group"
                >
                  <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-bold text-xl" style={{ backgroundColor: item.color }}>
                    {item.value}%
                  </div>
                  <div className="flex-1">
                    <h4 className="text-lg font-bold text-belgi-dark group-hover:text-belgi-gold transition-colors">{item.name}</h4>
                    <div className="w-full bg-belgi-dark/5 h-1.5 rounded-full mt-2 overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${item.value}%` }}
                        transition={{ duration: 1, delay: idx * 0.1 }}
                        className="h-full rounded-full"
                        style={{ backgroundColor: item.color }}
                      />
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Section 4: Prediction Engine */}
      <section id="prediction" className="py-24 px-6 md:px-20 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <span className="text-belgi-gold font-bold tracking-[0.3em] uppercase text-xs mb-4 block">AI-Powered Tool</span>
            <h2 className="text-5xl md:text-6xl font-serif font-bold text-belgi-dark mb-6">Predict Your Property Price</h2>
            <p className="text-belgi-dark/50 max-w-2xl mx-auto">
              Input property details and our model will estimate the market value based on current Belgian market data.
            </p>
          </div>

          <PredictionForm />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-belgi-dark py-20 px-6 md:px-20 border-t border-white/5">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <span className="text-3xl font-serif font-bold text-white mb-6 block">
              Belgi<span className="text-belgi-gold">Immo</span>
            </span>
            <p className="text-white/40 max-w-sm leading-relaxed mb-8">
              The definitive intelligence platform for the Belgian real estate market. Empowering buyers, sellers, and investors with data-driven clarity.
            </p>
            <div className="flex gap-4">
              {/* Social placeholders */}
              <div className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-belgi-gold hover:border-belgi-gold transition-all cursor-pointer">
                <Zap className="w-4 h-4" />
              </div>
              <div className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-belgi-gold hover:border-belgi-gold transition-all cursor-pointer">
                <Info className="w-4 h-4" />
              </div>
            </div>
          </div>
          
          <div>
            <h5 className="text-white font-bold uppercase tracking-widest text-xs mb-8">Platform</h5>
            <ul className="space-y-4 text-sm text-white/40">
              <li><a href="#" className="hover:text-white transition-colors">Market Analysis</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Price Prediction</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Regional Reports</a></li>
              <li><a href="#" className="hover:text-white transition-colors">API Access</a></li>
            </ul>
          </div>

          <div>
            <h5 className="text-white font-bold uppercase tracking-widest text-xs mb-8">Company</h5>
            <ul className="space-y-4 text-sm text-white/40">
              <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Data Methodology</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-20 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-white/20 text-xs">© 2026 BelgiImmo Intelligence. All rights reserved.</p>
          <div className="flex gap-8 text-xs text-white/20">
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-white transition-colors">Cookie Policy</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
