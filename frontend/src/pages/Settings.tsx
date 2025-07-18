import { useEffect, useState } from "react";
import { getConnectionStatus, saveSettings, testConnections } from "src/services/apiService";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
// ...outros imports...

export default function Settings() {
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    atcoinApiUrl: "",
    atcoinApiKey: "",
    binanceApiKey: "",
    binanceApiSecret: "",
    rebalanceInterval: "6",
    minTradeAmount: "10",
    autoRebalance: true,
    notifications: true
  });
  const { toast } = useToast();

  useEffect(() => {
    getConnectionStatus()
      .then((data) => {
        setIsConnected(data.isConnected); // Use the correct property name from ConnectionStatusResponse
        setFormData((prev) =      })
      .catch(() => setIsConnected(false))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        binanceApiKey: formData.binanceApiKey,
        binanceApiSecret: formData.binanceApiSecret,
        atcoinApiUrl: formData.atcoinApiUrl,
        atcoinApiKey: formData.atcoinApiKey,
        rebalanceInterval: "6",
        minTradeAmount: "10",
        autoRebalance: true,
        notifications: true
        // outros campos...
      })
    });
    // feedback ao usuário...
  };

  const handleTestConnections = async () => {
    toast({ title: "Testando conexões...", description: "Verificando conectividade com APIs." });
    try {
      const result = await testConnections();
      setIsConnected(result.connected);
      toast({ title: "Conexões testadas", description: "Todas as APIs estão respondendo corretamente." });
    } catch {
      setIsConnected(false);
      toast({ title: "Erro", description: "Falha ao testar conexões." });
    }
  };


}
