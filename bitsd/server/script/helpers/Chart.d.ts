declare var Chart: {
    new (ctx: any): ChartFactory;
}

interface ChartFactory {
    Line(data: LineData, options?: LineOptions): LineChart
}

declare class LineChart {
    constructor(data: LineData, options?: LineOptions)
}

interface LineData {
    labels?: string[];
    datasets: LineDataset[];
}

interface LineDataset {
    fillColor?: string;
    strokeColor?: string;
    pointColor?: string;
    pointStrokeColor?: string;
    data: number[];
}

interface LineOptions {
    scaleOverlay?: boolean;
    scaleOverride?: boolean;
    scaleSteps?: number;
    scaleStepWidth?: number;
    scaleStartValue?: number;
    scaleLineColor?: string;
    scaleLineWidth?: number;
    scaleShowLabels?: boolean;
    scaleLabel?: string;
    scaleFontFamily?: string;
    scaleFontSize?: number;
    scaleFontStyle?: string;
    scaleFontColor?: string;
    scaleShowGridLines?: boolean;
    scaleGridLineColor?: string;
    scaleGridLineWidth?: number;
    bezierCurve?: boolean;
    pointDot?: boolean;
    pointDotRadius?: number;
    pointDotStrokeWidth?: number;
    datasetStroke?: boolean;
    datasetStrokeWidth?: number;
    datasetFill?: boolean;
    animation?: boolean;
    animationSteps?: number;
    animationEasing?: string;
    onAnimationComplete?: Function;
}