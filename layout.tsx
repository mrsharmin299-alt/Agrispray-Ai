import "./globals.css";
export const metadata = { title: "AgriSpray AI", description: "আগাছা সনাক্তকরণ ও ফসল সুরক্ষা" };
export default function Root({ children }: { children: React.ReactNode }) {
  return (<html lang="bn"><head>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap" rel="stylesheet" />
  </head><body>{children}</body></html>);
}
