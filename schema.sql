CREATE TABLE IF NOT EXISTS weeds (
  id SERIAL PRIMARY KEY,
  name_bn TEXT NOT NULL, name_en TEXT, scientific_name TEXT,
  category TEXT CHECK (category IN ('grass','sedge','broadleaf')),
  features TEXT, reproduction TEXT, crops TEXT[], regions TEXT[],
  look_alikes TEXT, management TEXT, sources TEXT[],
  verified BOOLEAN DEFAULT FALSE, verified_at DATE,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS herbicides (
  id SERIAL PRIMARY KEY,
  brand TEXT NOT NULL, manufacturer TEXT, active_ingredient TEXT, formulation TEXT,
  registered_bd BOOLEAN,
  approved_crops TEXT[], approved_weeds TEXT[],
  label_instructions TEXT,
  plant_back_days JSONB,
  ppe TEXT, environment_notes TEXT,
  source_url TEXT, verified_at DATE
);
CREATE TABLE IF NOT EXISTS scans (
  id SERIAL PRIMARY KEY, image_path TEXT NOT NULL,
  status TEXT NOT NULL,
  result JSONB, created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS treatments (
  id SERIAL PRIMARY KEY, scan_id INT REFERENCES scans(id),
  herbicide_id INT REFERENCES herbicides(id), applied_on DATE,
  weather TEXT, notes TEXT, followup_image TEXT, outcome TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS audit_log (
  id SERIAL PRIMARY KEY, table_name TEXT, row_id INT, action TEXT,
  changed_by TEXT, detail JSONB, at TIMESTAMPTZ DEFAULT now()
);
