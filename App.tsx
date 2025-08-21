
import React, { useState, useCallback, useRef, useEffect } from 'react';
import type { CalibrationPoint, Sample, RegressionResults, CalculatedSample, Message, ParsedCalibrationPoint, ParsedSample } from './types';

// SVG Icons defined as components
const PlusIcon: React.FC<{ className?: string }> = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
);

const TrashIcon: React.FC<{ className?: string }> = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <polyline points="3 6 5 6 21 6"></polyline>
        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        <line x1="10" y1="11" x2="10" y2="17"></line>
        <line x1="14" y1="11" x2="14" y2="17"></line>
    </svg>
);

// --- Child Components defined outside the main App component ---

interface CalibrationTableProps {
    data: CalibrationPoint[];
    onUpdate: (index: number, field: keyof Omit<CalibrationPoint, 'id'>, value: string) => void;
    onAdd: () => void;
    onRemove: (id: number) => void;
}

const CalibrationTable: React.FC<CalibrationTableProps> = ({ data, onUpdate, onAdd, onRemove }) => {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-700">
                <thead className="text-xs text-gray-800 uppercase bg-gray-200">
                    <tr>
                        <th scope="col" className="px-6 py-3">Concentración de Proteína (X)</th>
                        <th scope="col" className="px-6 py-3">Densidad Óptica (Y)</th>
                        <th scope="col" className="px-6 py-3 w-28">Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={row.id} className="bg-white border-b hover:bg-gray-50">
                            <td className="px-6 py-2">
                                <input type="number" step="any" placeholder="Ej: 0 o 10.5" value={row.concentration} onChange={(e) => onUpdate(index, 'concentration', e.target.value)} className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"/>
                            </td>
                            <td className="px-6 py-2">
                                <input type="number" step="any" placeholder="Ej: 0.05 o 1.234" value={row.od} onChange={(e) => onUpdate(index, 'od', e.target.value)} className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"/>
                            </td>
                            <td className="px-6 py-2">
                                <button onClick={() => onRemove(row.id)} className="text-red-600 hover:text-red-800 p-2 rounded-full hover:bg-red-100 transition-colors">
                                    <TrashIcon className="w-5 h-5"/>
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={onAdd} className="mt-4 flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <PlusIcon className="w-4 h-4" />
                Añadir Estándar
            </button>
        </div>
    );
};

interface SamplesTableProps {
    data: Sample[];
    onUpdate: (index: number, field: keyof Omit<Sample, 'id'>, value: string) => void;
    onAdd: () => void;
    onRemove: (id: number) => void;
}

const SamplesTable: React.FC<SamplesTableProps> = ({ data, onUpdate, onAdd, onRemove }) => {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-700">
                <thead className="text-xs text-gray-800 uppercase bg-gray-200">
                    <tr>
                        <th scope="col" className="px-6 py-3">ID Muestra (Opcional)</th>
                        <th scope="col" className="px-6 py-3">Densidad Óptica de la Muestra</th>
                        <th scope="col" className="px-6 py-3">Factor de Dilución</th>
                        <th scope="col" className="px-6 py-3 w-28">Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={row.id} className="bg-white border-b hover:bg-gray-50">
                            <td className="px-6 py-2">
                                <input type="text" placeholder="Ej: Muestra A" value={row.sampleId} onChange={(e) => onUpdate(index, 'sampleId', e.target.value)} className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"/>
                            </td>
                            <td className="px-6 py-2">
                                <input type="number" step="any" placeholder="Ej: 0.750" value={row.od} onChange={(e) => onUpdate(index, 'od', e.target.value)} className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"/>
                            </td>
                            <td className="px-6 py-2">
                                <input type="number" step="any" placeholder="Ej: 1 o 10" value={row.dilution} onChange={(e) => onUpdate(index, 'dilution', e.target.value)} className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"/>
                            </td>
                            <td className="px-6 py-2">
                                <button onClick={() => onRemove(row.id)} className="text-red-600 hover:text-red-800 p-2 rounded-full hover:bg-red-100 transition-colors">
                                    <TrashIcon className="w-5 h-5"/>
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
             <button onClick={onAdd} className="mt-4 flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <PlusIcon className="w-4 h-4" />
                Añadir Muestra
            </button>
        </div>
    );
};

interface ResultsDisplayProps {
    regression: RegressionResults;
    calculatedSamples: CalculatedSample[];
    calibrationData: ParsedCalibrationPoint[];
    onExport: () => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ regression, calculatedSamples, calibrationData, onExport }) => {
    const plotRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (plotRef.current && (window as any).Plotly) {
            const traceCalibration = {
                x: calibrationData.map(p => p.x),
                y: calibrationData.map(p => p.y),
                mode: 'markers',
                type: 'scatter',
                name: 'Estándares de Calibración',
                marker: { color: '#2563eb', size: 10, symbol: 'circle' }
            };

            const minX = Math.min(...calibrationData.map(p => p.x));
            const maxX = Math.max(...calibrationData.map(p => p.x));
            const xRegression = [minX, maxX];
            const yRegression = xRegression.map(x => regression.slope * x + regression.intercept);

            const traceRegressionLine = {
                x: xRegression,
                y: yRegression,
                mode: 'lines',
                type: 'scatter',
                name: `Línea de Regresión (y = ${regression.slope.toFixed(4)}x + ${regression.intercept.toFixed(4)})`,
                line: { color: '#db2777', dash: 'dash' }
            };
            
            const traceSamples = {
                x: calculatedSamples.map(s => s.dilutedConcentration),
                y: calculatedSamples.map(s => s.od),
                mode: 'markers',
                type: 'scatter',
                name: 'Muestras (Conc. Diluida)',
                marker: { color: '#16a34a', size: 8, symbol: 'cross-thin' }
            };

            const layout = {
                title: 'Curva de Calibración y Muestras',
                xaxis: { title: 'Concentración de Proteína (Unidades X)', gridcolor: '#e5e7eb' },
                yaxis: { title: 'Densidad Óptica (Unidades Y)', gridcolor: '#e5e7eb' },
                legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(255,255,255,0.6)' },
                hovermode: 'closest',
                plot_bgcolor: '#f9fafb',
                paper_bgcolor: '#f9fafb',
            };

            (window as any).Plotly.newPlot(plotRef.current, [traceCalibration, traceRegressionLine, traceSamples], layout, {responsive: true});
        }
    }, [regression, calculatedSamples, calibrationData]);
    
    return (
        <div className="space-y-8">
            <div>
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Curva de Calibración</h3>
                <div ref={plotRef} className="w-full h-96 bg-gray-50 rounded-lg shadow-inner"></div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold text-gray-800 mb-6">Parámetros de Regresión</h3>
                <div className="space-y-4">
                    {/* Slope Row */}
                    <div className="flex flex-wrap justify-between items-center p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <div className="flex-grow pr-4">
                            <h4 className="font-semibold text-blue-800">Pendiente (b₁)</h4>
                            <p className="text-sm text-blue-700 mt-1">Mide la respuesta de la absorbancia por unidad de concentración.</p>
                        </div>
                        <p className="text-2xl font-bold text-blue-900 whitespace-nowrap">{regression.slope.toFixed(5)}</p>
                    </div>
                    {/* Intercept Row */}
                    <div className="flex flex-wrap justify-between items-center p-4 bg-pink-50 rounded-lg border border-pink-200">
                        <div className="flex-grow pr-4">
                            <h4 className="font-semibold text-pink-800">Intercepto (b₀)</h4>
                            <p className="text-sm text-pink-700 mt-1">La absorbancia teórica cuando la concentración es cero.</p>
                        </div>
                        <p className="text-2xl font-bold text-pink-900 whitespace-nowrap">{regression.intercept.toFixed(5)}</p>
                    </div>
                    {/* R-Squared Row */}
                    <div className="flex flex-wrap justify-between items-center p-4 bg-green-50 rounded-lg border border-green-200">
                        <div className="flex-grow pr-4">
                            <h4 className="font-semibold text-green-800">Coeficiente de Determinación (R²)</h4>
                            <p className="text-sm text-green-700 mt-1">Indica qué tan bien los datos se ajustan a la línea (cercano a 1 es mejor).</p>
                        </div>
                        <p className="text-2xl font-bold text-green-900 whitespace-nowrap">{regression.rSquared.toFixed(4)}</p>
                    </div>
                </div>
            </div>

            <div>
                 <h3 className="text-xl font-semibold text-gray-800 mb-4">Concentraciones de Muestras Calculadas</h3>
                <div className="overflow-x-auto bg-white rounded-lg shadow-md">
                     <table className="w-full text-sm text-left text-gray-700">
                        <thead className="text-xs text-gray-800 uppercase bg-gray-200">
                            <tr>
                                <th scope="col" className="px-6 py-3">ID Muestra</th>
                                <th scope="col" className="px-6 py-3">DO Ingresada</th>
                                <th scope="col" className="px-6 py-3">Dilución</th>
                                <th scope="col" className="px-6 py-3">Conc. Calculada (Diluida)</th>
                                <th scope="col" className="px-6 py-3">Conc. Final (Original)</th>
                                <th scope="col" className="px-6 py-3">Notas</th>
                            </tr>
                        </thead>
                        <tbody>
                            {calculatedSamples.map((sample) => (
                                <tr key={sample.id} className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4 font-medium text-gray-900">{sample.sampleId}</td>
                                    <td className="px-6 py-4">{sample.od.toFixed(3)}</td>
                                    <td className="px-6 py-4">{sample.dilution}</td>
                                    <td className="px-6 py-4 font-semibold">{sample.dilutedConcentration.toFixed(3)}</td>
                                    <td className="px-6 py-4 font-bold text-blue-700">{sample.finalConcentration.toFixed(3)}</td>
                                    <td className="px-6 py-4 text-xs">{sample.notes || '-'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <button onClick={onExport} className="mt-4 px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                    Exportar Resultados a CSV
                </button>
            </div>
        </div>
    );
};

// --- Main App Component ---

const App: React.FC = () => {
    const initialCalibrationData: CalibrationPoint[] = [
        { id: 1, concentration: '0', od: '0.05' },
        { id: 2, concentration: '10', od: '0.25' },
        { id: 3, concentration: '20', od: '0.48' },
        { id: 4, concentration: '30', od: '0.65' },
        { id: 5, concentration: '40', od: '0.90' },
    ];
    const initialSampleData: Sample[] = [
        { id: 1, sampleId: 'Muestra 1', od: '0.35', dilution: '2' },
        { id: 2, sampleId: 'Muestra 2', od: '0.70', dilution: '1' },
        { id: 3, sampleId: 'Muestra 3', od: '0.10', dilution: '1' },
        { id: 4, sampleId: 'Muestra 4', od: '1.20', dilution: '5' },
    ];

    const [calibrationData, setCalibrationData] = useState<CalibrationPoint[]>(initialCalibrationData);
    const [sampleData, setSampleData] = useState<Sample[]>(initialSampleData);
    
    const [results, setResults] = useState<{
        regression: RegressionResults,
        calculatedSamples: CalculatedSample[],
        parsedCalibration: ParsedCalibrationPoint[]
    } | null>(null);
    
    const [messages, setMessages] = useState<Message[]>([]);

    const handleCalibrationUpdate = useCallback((index: number, field: keyof Omit<CalibrationPoint, 'id'>, value: string) => {
        setCalibrationData(current => {
            const newData = [...current];
            newData[index] = { ...newData[index], [field]: value };
            return newData;
        });
    }, []);

    const addCalibrationRow = useCallback(() => {
        setCalibrationData(current => [...current, { id: Date.now(), concentration: '', od: '' }]);
    }, []);

    const removeCalibrationRow = useCallback((id: number) => {
        setCalibrationData(current => current.filter(row => row.id !== id));
    }, []);

    const handleSampleUpdate = useCallback((index: number, field: keyof Omit<Sample, 'id'>, value: string) => {
        setSampleData(current => {
            const newData = [...current];
            newData[index] = { ...newData[index], [field]: value };
            return newData;
        });
    }, []);

    const addSampleRow = useCallback(() => {
        setSampleData(current => {
             const newId = `Muestra ${current.length + 1}`;
             return [...current, { id: Date.now(), sampleId: newId, od: '', dilution: '1' }];
        });
    }, []);

    const removeSampleRow = useCallback((id: number) => {
        setSampleData(current => current.filter(row => row.id !== id));
    }, []);

    const handleCalculate = () => {
        setMessages([]);
        setResults(null);
        let newMessages: Message[] = [];
        let isValid = true;

        // --- Validation ---
        const parsedCalibration: ParsedCalibrationPoint[] = [];
        calibrationData.forEach((row, index) => {
            const conc = parseFloat(row.concentration);
            const od = parseFloat(row.od);
            if (isNaN(conc) || isNaN(od)) {
                newMessages.push({ text: `Error: Datos de calibración inválidos en la fila ${index + 1}. Ingrese solo números.`, type: 'error' });
                isValid = false;
            } else {
                if (conc < 0 || od < 0) {
                    newMessages.push({ text: `Advertencia: Concentración o DO negativa en la fila de calibración ${index + 1}. Se recomienda revisar.`, type: 'warning' });
                }
                parsedCalibration.push({ x: conc, y: od });
            }
        });

        if (parsedCalibration.length < 3) {
            newMessages.push({ text: 'Error: Se requieren al menos 3 puntos de calibración.', type: 'error' });
            isValid = false;
        }
        if (!parsedCalibration.some(p => p.x === 0)) {
            newMessages.push({ text: 'Error: La curva de calibración debe incluir un blanco (Concentración = 0).', type: 'error' });
            isValid = false;
        }

        const parsedSamples: ParsedSample[] = [];
        sampleData.forEach((row, index) => {
            const od = parseFloat(row.od);
            const dilution = parseFloat(row.dilution);
            if (isNaN(od) || isNaN(dilution)) {
                newMessages.push({ text: `Error: Datos de muestra inválidos en la fila ${index + 1}. Ingrese solo números.`, type: 'error' });
                isValid = false;
            } else if (dilution <= 0) {
                 newMessages.push({ text: `Error: El factor de dilución para la muestra "${row.sampleId}" debe ser mayor que cero.`, type: 'error' });
                 isValid = false;
            } else {
                 if (od < 0) {
                    newMessages.push({ text: `Advertencia: Densidad Óptica negativa para la muestra "${row.sampleId}". Se recomienda revisar.`, type: 'warning' });
                }
                parsedSamples.push({ id: row.sampleId || `Muestra ${index + 1}`, od, dilution });
            }
        });
        
        setMessages(newMessages);
        if (!isValid) return;

        // --- Linear Regression Calculation ---
        const n = parsedCalibration.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0, sumYY = 0;
        parsedCalibration.forEach(p => {
            sumX += p.x; sumY += p.y; sumXY += p.x * p.y; sumXX += p.x * p.x; sumYY += p.y * p.y;
        });

        const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        const rNumerator = (n * sumXY - sumX * sumY);
        const rDenominator = Math.sqrt((n * sumXX - sumX * sumX) * (n * sumYY - sumY * sumY));
        const rSquared = rDenominator === 0 ? 1 : Math.pow(rNumerator / rDenominator, 2);

        if (isNaN(slope) || isNaN(intercept)) {
            setMessages(m => [...m, {text: 'Error: No se pudo calcular la regresión. Verifique si hay puntos de calibración duplicados o datos inválidos.', type: 'error'}]);
            return;
        }
        if (Math.abs(slope) < 1e-9) {
            setMessages(m => [...m, {text: 'Error: La curva de calibración tiene una pendiente cercana a cero. No se pueden calcular las concentraciones.', type: 'error'}]);
            return;
        }
        
        const regression: RegressionResults = { slope, intercept, rSquared };

        // --- Sample Concentration Calculation ---
        const minCalibrationOD = Math.min(...parsedCalibration.map(p => p.y));
        const maxCalibrationOD = Math.max(...parsedCalibration.map(p => p.y));
        const calculationWarnings: Message[] = [];

        const calculatedSamples: CalculatedSample[] = sampleData.map((sample, i) => {
            const ps = parsedSamples[i];
            const dilutedConcentration = (ps.od - intercept) / slope;
            const finalConcentration = dilutedConcentration * ps.dilution;
            let notes = "";

            if (dilutedConcentration < 0) {
                notes += "La concentración calculada es negativa. ";
                calculationWarnings.push({ text: `Advertencia: La concentración calculada para la muestra "${ps.id}" es negativa. El resultado puede estar por debajo del límite de detección.`, type: 'warning' });
            }
            if (ps.od < minCalibrationOD || ps.od > maxCalibrationOD) {
                notes += "La DO está fuera del rango de calibración (extrapolado).";
                calculationWarnings.push({ text: `Advertencia: La DO para la muestra "${ps.id}" (${ps.od.toFixed(3)}) está fuera del rango de calibración (${minCalibrationOD.toFixed(3)} - ${maxCalibrationOD.toFixed(3)}). El resultado es una extrapolación.`, type: 'warning' });
            }
            return {
                id: sample.id,
                sampleId: ps.id,
                od: ps.od,
                dilution: ps.dilution,
                dilutedConcentration,
                finalConcentration,
                notes,
            };
        });

        setResults({ regression, calculatedSamples, parsedCalibration });
        setMessages(m => [...m, ...calculationWarnings]);
    };
    
    const handleExportCSV = useCallback(() => {
        if (!results) return;
        
        let csvContent = "data:text/csv;charset=utf-8,";
        const headers = ["ID Muestra", "DO Ingresada", "Dilución", "Conc. Calculada (Diluida)", "Conc. Final (Original)", "Notas"];
        csvContent += headers.join(',') + "\r\n";

        results.calculatedSamples.forEach(row => {
            const rowData = [
                `"${row.sampleId.replace(/"/g, '""')}"`,
                row.od.toFixed(3),
                row.dilution,
                row.dilutedConcentration.toFixed(3),
                row.finalConcentration.toFixed(3),
                `"${row.notes.replace(/"/g, '""')}"`
            ];
            csvContent += rowData.join(',') + "\r\n";
        });
        
        csvContent += "\r\nParámetros de Regresión\r\n";
        csvContent += `Pendiente (b1),${results.regression.slope.toFixed(5)}\r\n`;
        csvContent += `Intercepto (b0),${results.regression.intercept.toFixed(5)}\r\n`;
        csvContent += `Coeficiente de Determinación (R²),${results.regression.rSquared.toFixed(4)}\r\n`;

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "resultados_ensayo_proteinas.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }, [results]);

    return (
        <div className="container mx-auto p-4 md:p-8 max-w-6xl">
            <header className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-800">Calculadora de Concentración de Proteínas</h1>
                <p className="text-lg text-gray-600 mt-2">Usando regresión lineal a partir de una curva estándar</p>
            </header>

            <div className="space-y-4 mb-8">
                {messages.map((msg, i) => (
                    <div key={i} className={`p-4 rounded-md text-sm ${msg.type === 'error' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`} role="alert">
                        <span className="font-medium">{msg.type.charAt(0).toUpperCase() + msg.type.slice(1)}:</span> {msg.text}
                    </div>
                ))}
            </div>

            <main className="space-y-12">
                <section className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-2">1. Datos de la Curva de Calibración</h2>
                    <p className="text-sm text-gray-600 mb-4">
                        Introduzca al menos 3 estándares. <strong>Incluya siempre un blanco (Concentración = 0).</strong> Los estándares deben cubrir el rango de DO esperado de sus muestras.
                    </p>
                    <CalibrationTable data={calibrationData} onUpdate={handleCalibrationUpdate} onAdd={addCalibrationRow} onRemove={removeCalibrationRow} />
                </section>

                <section className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-2">2. Datos de Muestras</h2>
                    <p className="text-sm text-gray-600 mb-4">
                        El "Factor de Dilución" es un valor numérico (ej: para una dilución 1:10, introducir '10'). Use '1' para muestras no diluidas.
                    </p>
                    <SamplesTable data={sampleData} onUpdate={handleSampleUpdate} onAdd={addSampleRow} onRemove={removeSampleRow} />
                </section>

                <div className="text-center py-4">
                    <button onClick={handleCalculate} className="px-8 py-3 text-lg font-semibold text-white bg-green-600 rounded-lg shadow-lg hover:bg-green-700 focus:outline-none focus:ring-4 focus:ring-green-300 transition-transform transform hover:scale-105">
                        Calcular Resultados
                    </button>
                </div>

                {results && (
                    <section id="resultsSection" className="bg-gray-50 p-6 rounded-lg shadow-inner mt-12">
                         <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">3. Resultados</h2>
                         <ResultsDisplay 
                            regression={results.regression} 
                            calculatedSamples={results.calculatedSamples} 
                            calibrationData={results.parsedCalibration}
                            onExport={handleExportCSV}
                         />
                    </section>
                )}
            </main>
             <footer className="text-center mt-12 text-sm text-gray-500">
                <p>&copy; 2024 App Calculadora de Proteínas. Creada con React y Tailwind CSS.</p>
            </footer>
        </div>
    );
};

export default App;
