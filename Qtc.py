import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectItem } from "@/components/ui/select";
import { Line } from "recharts";
import { ResponsiveContainer, LineChart, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function QTcCalculator() {
  const [qt, setQt] = useState(0);
  const [fc, setFc] = useState(60);
  const [rr, setRr] = useState(1);
  const [method, setMethod] = useState("Bazett");
  const [sex, setSex] = useState("Homme");
  const [qtInputType, setQtInputType] = useState("Millisecondes");
  const [qtc, setQtc] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [search, setSearch] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const storedHistory = JSON.parse(localStorage.getItem("qtcHistory")) || [];
    setHistory(storedHistory);
  }, []);

  const calculateQtc = async () => {
    let qtValue = qt;
    if (qtInputType === "Petits carreaux") {
      qtValue *= 40;
    }
    
    const response = await fetch("http://localhost:8000/calculate_qtc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ qt: qtValue, fc, rr, method }),
    });
    const data = await response.json();
    setQtc(data.qtc);

    const newChartData = Array.from({ length: 100 }, (_, i) => {
      const x = 300 + i * 2.5;
      const y = Math.exp(-0.5 * ((x - 400) / 30) ** 2) / (30 * Math.sqrt(2 * Math.PI));
      return { qtc: x, density: y };
    });
    setChartData(newChartData);

    const newHistory = [...history, { qt: qtValue, fc, rr, method, qtc: data.qtc }];
    setHistory(newHistory);
    localStorage.setItem("qtcHistory", JSON.stringify(newHistory));
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      
      <Card className="w-full max-w-md p-4">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Qu'est-ce que le QT ?</h2>
          <p>
            L’intervalle QT est la durée entre le début de la dépolarisation ventriculaire et la fin de la repolarisation.
            Une prolongation peut entraîner un risque accru d’arythmies graves.
          </p>
        </CardContent>
      </Card>

      <Card className="w-full max-w-md p-4 mt-6">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Pourquoi est-il nécessaire de calculer le QT corrigé ?</h2>
          <p>
            Le QT varie selon la fréquence cardiaque, et le QTc permet de standardiser la mesure
            afin d'évaluer correctement le risque d’arythmie.
          </p>
        </CardContent>
      </Card>

      <Card className="w-full max-w-md p-4 mt-6">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Comment calculer le QT corrigé ?</h2>
          <p>
            Différentes formules existent : Bazett, Fridericia, Framingham et Hodges.
            Chacune a des avantages et inconvénients selon la fréquence cardiaque du patient.
          </p>
        </CardContent>
      </Card>

      <Card className="w-full max-w-md p-4 mt-6">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Maladies augmentant le QT</h2>
          <p>
            Hypokaliémie, syndrome du QT long congénital, hypothyroïdie, insuffisance cardiaque, etc.
          </p>
        </CardContent>
      </Card>

      <Card className="w-full max-w-md p-4 mt-6">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Drogues et médicaments augmentant le QT</h2>
          <p>
            Antipsychotiques, antibiotiques macrolides, antidépresseurs tricycliques, etc.
          </p>
        </CardContent>
      </Card>
      
      <Card className="w-full max-w-md p-4 mt-6">
        <CardContent>
          <h2 className="text-xl font-bold mb-4">Programme de calcul du QT corrigé</h2>
          <Select value={qtInputType} onChange={(e) => setQtInputType(e.target.value)} className="mb-2">
            <SelectItem value="Millisecondes">Millisecondes</SelectItem>
            <SelectItem value="Petits carreaux">Petits carreaux</SelectItem>
          </Select>
          <Input type="number" value={qt} onChange={(e) => setQt(parseFloat(e.target.value))} placeholder="QT" className="mb-2" />
          <Input type="number" value={fc} onChange={(e) => setFc(parseFloat(e.target.value))} placeholder="Fréquence cardiaque (BPM)" className="mb-2" />
          <Input type="number" value={rr} onChange={(e) => setRr(parseFloat(e.target.value))} placeholder="Intervalle RR (s)" className="mb-2" />
          <Button onClick={calculateQtc} className="w-full">Calculer QTc</Button>
        </CardContent>
      </Card>
    </div>
  );
}

