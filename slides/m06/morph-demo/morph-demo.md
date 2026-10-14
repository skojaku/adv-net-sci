---
marp: true
theme: network-science
transition: fade
---

<style>
::view-transition-group(*) { animation-duration: .8s; animation-timing-function: ease-in-out; }
</style>

## Degree

<hr>

How many neighbours? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 320" width="1080" height="320" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="150" x2="220" y2="15" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="87" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="213" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="220" y2="285" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="490" y2="150" stroke="#555" stroke-width="3"/>
<line x1="490" y1="150" x2="685" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="60" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="60" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="918" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="240" x2="955" y2="298" stroke="#555" stroke-width="3"/>
<circle cx="220" cy="15" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<circle cx="100" cy="87" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<circle cx="100" cy="213" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<circle cx="220" cy="285" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<circle cx="220" cy="150" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<circle cx="490" cy="150" r="17.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<circle cx="685" cy="150" r="28.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<circle cx="805" cy="60" r="17.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<circle cx="918" cy="150" r="23.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<circle cx="805" cy="240" r="23.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<circle cx="955" cy="298" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="220" y="22" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">A</text>
<text x="100" y="94" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">B</text>
<text x="100" y="220" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">C</text>
<text x="220" y="292" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">D</text>
<text x="220" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">E</text>
<text x="490" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">F</text>
<text x="685" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">G</text>
<text x="805" y="67" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">H</text>
<text x="918" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">I</text>
<text x="805" y="247" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">J</text>
<text x="955" y="306" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">K</text>
</svg>

</div>

<div class="cue">

*E has five neighbours and wins.*

</div>


---

## Closeness

<hr>

How near is everyone? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 320" width="1080" height="320" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="150" x2="220" y2="15" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="87" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="213" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="220" y2="285" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="490" y2="150" stroke="#555" stroke-width="3"/>
<line x1="490" y1="150" x2="685" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="60" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="60" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="918" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="240" x2="955" y2="298" stroke="#555" stroke-width="3"/>
<circle cx="220" cy="15" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<circle cx="100" cy="87" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<circle cx="100" cy="213" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<circle cx="220" cy="285" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<circle cx="220" cy="150" r="31.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<circle cx="490" cy="150" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<circle cx="685" cy="150" r="31.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<circle cx="805" cy="60" r="18.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<circle cx="918" cy="150" r="21.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<circle cx="805" cy="240" r="21.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<circle cx="955" cy="298" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="220" y="22" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">A</text>
<text x="100" y="94" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">B</text>
<text x="100" y="220" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">C</text>
<text x="220" y="292" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">D</text>
<text x="220" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">E</text>
<text x="490" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">F</text>
<text x="685" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">G</text>
<text x="805" y="67" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">H</text>
<text x="918" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">I</text>
<text x="805" y="247" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">J</text>
<text x="955" y="306" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">K</text>
</svg>

</div>

<div class="cue">

*F, with two neighbours, takes the crown.*

</div>


---

## Betweenness

<hr>

How many shortest paths pass through? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 320" width="1080" height="320" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="150" x2="220" y2="15" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="87" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="100" y2="213" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="220" y2="285" stroke="#555" stroke-width="3"/>
<line x1="220" y1="150" x2="490" y2="150" stroke="#555" stroke-width="3"/>
<line x1="490" y1="150" x2="685" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="60" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="685" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="60" x2="918" y2="150" stroke="#555" stroke-width="3"/>
<line x1="918" y1="150" x2="805" y2="240" stroke="#555" stroke-width="3"/>
<line x1="805" y1="240" x2="955" y2="298" stroke="#555" stroke-width="3"/>
<circle cx="220" cy="15" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<circle cx="100" cy="87" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<circle cx="100" cy="213" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<circle cx="220" cy="285" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<circle cx="220" cy="150" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<circle cx="490" cy="150" r="30.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<circle cx="685" cy="150" r="30.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<circle cx="805" cy="60" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<circle cx="918" cy="150" r="12.7" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<circle cx="805" cy="240" r="18.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<circle cx="955" cy="298" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="220" y="22" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">A</text>
<text x="100" y="94" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">B</text>
<text x="100" y="220" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">C</text>
<text x="220" y="292" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">D</text>
<text x="220" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">E</text>
<text x="490" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">F</text>
<text x="685" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">G</text>
<text x="805" y="67" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">H</text>
<text x="918" y="157" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">I</text>
<text x="805" y="247" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">J</text>
<text x="955" y="306" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6">K</text>
</svg>

</div>

<div class="cue">

*E again. F and G tie for second, at 25.*

</div>
