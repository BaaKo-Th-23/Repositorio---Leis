// OCR de PDF com o framework Vision do macOS (sem dependências externas).
// Uso: ocr arquivo.pdf  -> texto em UTF-8 no stdout, páginas separadas por \f
import AppKit
import Foundation
import PDFKit
import Vision

guard CommandLine.arguments.count > 1,
      let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1])) else {
    FileHandle.standardError.write("uso: ocr arquivo.pdf\n".data(using: .utf8)!)
    exit(2)
}

let escala: CGFloat = 2.5  // ~180 dpi: bom equilíbrio entre precisão e tempo
var saida = ""

for i in 0..<doc.pageCount {
    guard let pagina = doc.page(at: i) else { continue }
    let caixa = pagina.bounds(for: .mediaBox)
    let largura = Int(caixa.width * escala), altura = Int(caixa.height * escala)
    guard let ctx = CGContext(data: nil, width: largura, height: altura, bitsPerComponent: 8, bytesPerRow: 0,
                              space: CGColorSpaceCreateDeviceRGB(),
                              bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { continue }
    ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: largura, height: altura))
    ctx.scaleBy(x: escala, y: escala)
    pagina.draw(with: .mediaBox, to: ctx)
    guard let imagem = ctx.makeImage() else { continue }

    let pedido = VNRecognizeTextRequest()
    pedido.recognitionLevel = .accurate
    pedido.recognitionLanguages = ["pt-BR"]
    pedido.usesLanguageCorrection = true
    try? VNImageRequestHandler(cgImage: imagem, options: [:]).perform([pedido])

    // ordena as linhas de cima para baixo (Vision usa origem no canto inferior esquerdo)
    let linhas = (pedido.results ?? [])
        .sorted { $0.boundingBox.maxY > $1.boundingBox.maxY }
        .compactMap { $0.topCandidates(1).first?.string }
    saida += linhas.joined(separator: "\n") + "\n\u{0C}"
}

FileHandle.standardOutput.write(saida.data(using: .utf8)!)
