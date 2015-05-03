\def\@universidad{Universidad}
\newcommand{\universidad}[1]{
  \def\@universidad{#1}
}

\def\@titulo{Campo título vacío!}
\newcommand{\titulo}[1]{
  \gdef\@titulo{#1}
}

\def\@autores{Campo autores vacío!}
\newcommand{\autores}[1]{
  \gdef\@autores{#1}
}

\maketitle

\renewcommand{\maketitle}{
  {\@universidad}\\
  %{\@universidad}\\
}
