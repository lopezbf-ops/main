
export interface CalibrationPoint {
  id: number;
  concentration: string;
  od: string;
}

export interface Sample {
  id: number;
  sampleId: string;
  od: string;
  dilution: string;
}

export interface RegressionResults {
  slope: number;
  intercept: number;
  rSquared: number;
}

export interface CalculatedSample {
  id: number;
  sampleId: string;
  od: number;
  dilution: number;
  dilutedConcentration: number;
  finalConcentration: number;
  notes: string;
}

export interface Message {
  text: string;
  type: 'error' | 'warning';
}

export interface ParsedCalibrationPoint {
  x: number;
  y: number;
}

export interface ParsedSample {
  id: string;
  od: number;
  dilution: number;
}
