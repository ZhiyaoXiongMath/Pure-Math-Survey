# S02 source rereading for exponential covering and triangle globalization

Date: 2026-10-12. Mode: author reading, by the candidate author and then the S02 main integrator. Neither role is an independent nonauthor gate reviewer.

## Materials and actual reads

Lang, *Riemannian and Metric Geometry*, preliminary and incomplete version dated 5 January 2026. The registered 144-page PDF has SHA-256 931ce2b70009721e37fdf4454c8687990894f403086c933e94547020eddb0e2e. Printed body page \(n\) is physical page \(n+4\). The candidate author read the title page, printed p. 14, pp. 43–44 and pp. 63–70, and visually inspected pp. 67–70. The main integrator separately read printed p. 14, pp. 43–44 and pp. 65–70 from the original PDF, and visually inspected the full printed p. 70. The record is the [registered source](../../knowledge/sources/S-Lang-2026.json); the original text is [Lang's author-hosted PDF](https://people.math.ethz.ch/~lang/RG.pdf).

Bishop, *Riemannian Geometry*, arXiv:1303.5390v2, 27 July 2013. SHA-256 661745181375a3fe6302d2e510ca8e628eed4ae24b3fa866745a43b292b2b1a8. Printed and physical page numbers agree in the read sections. The candidate author read the title page, pp. 33–34, 52–55 and visually inspected p. 55. The main integrator's independent author reread included pp. 33–34, 45–46, 53–56 and the full image of p. 55. See the [registered source](../../knowledge/sources/S-Bishop-2013v2.json) and the [radial-route reading note](S02-radial-route-20261012.md).

“Separately read” here describes two author-side readings, not independent review in the staged acceptance process. Source PDFs and rendered images remain in private work/cache locations and are excluded from the knowledge packet.

## Supported interfaces and local operations

Lang Corollaries 3.20–3.21 support the conversion from Jacobi fields to the exponential differential and the direction of local length comparison: a model of curvature \(k\) maps to the manifold of curvature at least \(k\), and the map contracts lengths on their common normal domain. The revised node derives both radial/angular components and proves that the chosen model chord stays inside that domain.

Lang Corollary 1.22's proof and Theorem 5.12 use a normal radius uniform for nearby centers. The revision states that input through the local map \((p,\xi)\mapsto(p,\exp_p\xi)\) and applies it at the moving vertices of the shrinking hinges.

Lang Definition 5.7 distinguishes SSS angle/chord comparison from the same-angle hinge experiment. Lemma 5.9's lower-curvature direction needs balanced original sides and angle comparison for all connecting hinges. The revision checks their perimeters by an explicit path-length sum, rather than substituting the angle estimate of one original hinge.

Propositions 5.13–5.14 assume balanced segments and existence of a minimizing segment whenever the distance is \(<D_k\). The revision preserves the thin-side hypotheses of 5.13, the exact endpoint condition in 5.14, and the strict perimeter. It allows the degenerate auxiliary hinges admitted by those lemmas without changing the nondegenerate principal theorem. The \(4/5\) contraction then yields the actual successive-displacement factor \(9/5\) and the geometric-series tail factor \(9\).

Bishop Theorem 9.2 gives the pullback-metric route to covering. The revision checks the entire radial geodesics from zero, uses the one-point Hopf--Rinow criterion, and constructs the inverse branches on a normal ball. It distinguishes local invertibility, a covering and one-sheetedness.

## Source corrections established visually

Lang printed p. 70 shows \(4/5\) in every shrinking occurrence, including the recursive perimeter estimate. The old mechanism's assertion that the source printed \(5/4\) once was false for these registered bytes. It arose from fraction extraction order and is removed. The full page image is the direct visual evidence; an earlier attempted narrow crop cuts off the relevant line and is not used as the main integrator's evidence.

Bishop printed p. 55 really omits a factor \(2\) in the curvature summand of the squared-Jacobi-norm second derivative. Both author-side image inspections confirm this. The revised identity is obtained by differentiating locally, \((|J|^2)''=2|J'|^2-2\langle R(J,T)T,J\rangle\). The convexity and no-second-zero conclusion is unchanged.

## Limits

The technical gluing proofs, the angle-to-chord conversion proof, Hopf--Rinow, preservation of the connection by local isometries and basic covering-space topology remain declared imports. The original 1959 Toponogov paper was not newly reread during this revision; its older source record and limited original-angle support remain unchanged. No expanded endpoint, equality, nonminimizing-hinge or synthetic theorem is claimed.
