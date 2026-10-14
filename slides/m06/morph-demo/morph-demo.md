---
marp: true
theme: network-science
transition: fade
---

<style>
/* 0.8s unless the slide's own `transition: fade 1.6s` asks for longer; Marp exposes it as this variable (-1s when unset) */
::view-transition-group(*) { animation-duration: max(.8s, var(--marp-bespoke-transition-animation-duration)); animation-timing-function: ease-in-out; }
</style>

<!-- _transition: fade -->

## Degree

<hr>

How many neighbours? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 335" width="1080" height="335" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="30" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_AE"/>
<line x1="100" y1="102" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_BE"/>
<line x1="100" y1="228" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_CE"/>
<line x1="220" y1="300" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_DE"/>
<line x1="220" y1="165" x2="490" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_EF"/>
<line x1="490" y1="165" x2="685" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_FG"/>
<line x1="685" y1="165" x2="805" y2="75" stroke="#555" stroke-width="3" style="view-transition-name:e_GH"/>
<line x1="685" y1="165" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_GI"/>
<line x1="685" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_GJ"/>
<line x1="805" y1="75" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_HI"/>
<line x1="918" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_IJ"/>
<line x1="805" y1="255" x2="955" y2="314" stroke="#555" stroke-width="3" style="view-transition-name:e_JK"/>
<circle cx="220" cy="30" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<text x="220" y="37" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_A">A</text>
<circle cx="100" cy="102" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<text x="100" y="109" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_B">B</text>
<circle cx="100" cy="228" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<text x="100" y="235" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_C">C</text>
<circle cx="220" cy="300" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<text x="220" y="307" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_D">D</text>
<circle cx="220" cy="165" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<text x="220" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_E">E</text>
<circle cx="490" cy="165" r="17.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<text x="490" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_F">F</text>
<circle cx="685" cy="165" r="28.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<text x="685" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_G">G</text>
<circle cx="805" cy="75" r="17.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<text x="805" y="82" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_H">H</text>
<circle cx="918" cy="165" r="23.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<text x="918" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_I">I</text>
<circle cx="805" cy="255" r="23.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<text x="805" y="262" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_J">J</text>
<circle cx="955" cy="314" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="955" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_K">K</text>
</svg>

</div>

<div class="cue">

*E has five neighbours and wins.*

</div>


---

<!-- _transition: fade -->

## Closeness

<hr>

How near is everyone? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 335" width="1080" height="335" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="30" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_AE"/>
<line x1="100" y1="102" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_BE"/>
<line x1="100" y1="228" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_CE"/>
<line x1="220" y1="300" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_DE"/>
<line x1="220" y1="165" x2="490" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_EF"/>
<line x1="490" y1="165" x2="685" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_FG"/>
<line x1="685" y1="165" x2="805" y2="75" stroke="#555" stroke-width="3" style="view-transition-name:e_GH"/>
<line x1="685" y1="165" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_GI"/>
<line x1="685" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_GJ"/>
<line x1="805" y1="75" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_HI"/>
<line x1="918" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_IJ"/>
<line x1="805" y1="255" x2="955" y2="314" stroke="#555" stroke-width="3" style="view-transition-name:e_JK"/>
<circle cx="220" cy="30" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<text x="220" y="37" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_A">A</text>
<circle cx="100" cy="102" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<text x="100" y="109" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_B">B</text>
<circle cx="100" cy="228" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<text x="100" y="235" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_C">C</text>
<circle cx="220" cy="300" r="17.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<text x="220" y="307" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_D">D</text>
<circle cx="220" cy="165" r="31.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<text x="220" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_E">E</text>
<circle cx="490" cy="165" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<text x="490" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_F">F</text>
<circle cx="685" cy="165" r="31.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<text x="685" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_G">G</text>
<circle cx="805" cy="75" r="18.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<text x="805" y="82" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_H">H</text>
<circle cx="918" cy="165" r="21.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<text x="918" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_I">I</text>
<circle cx="805" cy="255" r="21.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<text x="805" y="262" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_J">J</text>
<circle cx="955" cy="314" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="955" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_K">K</text>
</svg>

</div>

<div class="cue">

*F, with two neighbours, takes the crown.*

</div>


---

<!-- _transition: fade -->

## Betweenness

<hr>

How many shortest paths pass through? Disc size is the score, rescaled from the smallest to the largest.

<div class="fig">

<svg viewBox="0 0 1080 335" width="1080" height="335" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="30" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_AE"/>
<line x1="100" y1="102" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_BE"/>
<line x1="100" y1="228" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_CE"/>
<line x1="220" y1="300" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_DE"/>
<line x1="220" y1="165" x2="490" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_EF"/>
<line x1="490" y1="165" x2="685" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_FG"/>
<line x1="685" y1="165" x2="805" y2="75" stroke="#555" stroke-width="3" style="view-transition-name:e_GH"/>
<line x1="685" y1="165" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_GI"/>
<line x1="685" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_GJ"/>
<line x1="805" y1="75" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_HI"/>
<line x1="918" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_IJ"/>
<line x1="805" y1="255" x2="955" y2="314" stroke="#555" stroke-width="3" style="view-transition-name:e_JK"/>
<circle cx="220" cy="30" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<text x="220" y="37" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_A">A</text>
<circle cx="100" cy="102" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<text x="100" y="109" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_B">B</text>
<circle cx="100" cy="228" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<text x="100" y="235" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_C">C</text>
<circle cx="220" cy="300" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<text x="220" y="307" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_D">D</text>
<circle cx="220" cy="165" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<text x="220" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_E">E</text>
<circle cx="490" cy="165" r="30.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<text x="490" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_F">F</text>
<circle cx="685" cy="165" r="30.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<text x="685" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_G">G</text>
<circle cx="805" cy="75" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<text x="805" y="82" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_H">H</text>
<circle cx="918" cy="165" r="12.7" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<text x="918" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_I">I</text>
<circle cx="805" cy="255" r="18.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<text x="805" y="262" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_J">J</text>
<circle cx="955" cy="314" r="12.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="955" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_K">K</text>
</svg>

</div>

<div class="cue">

*E again. F and G tie for second, at 25.*

</div>


---

<!-- _transition: fade -->

## Harmonic

<hr>

Add 1/distance over everyone. Size is the score on one common scale.

<div class="fig">

<svg viewBox="0 0 1080 335" width="1080" height="335" xmlns="http://www.w3.org/2000/svg">
<line x1="220" y1="30" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_AE"/>
<line x1="100" y1="102" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_BE"/>
<line x1="100" y1="228" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_CE"/>
<line x1="220" y1="300" x2="220" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_DE"/>
<line x1="220" y1="165" x2="490" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_EF"/>
<line x1="490" y1="165" x2="685" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_FG"/>
<line x1="685" y1="165" x2="805" y2="75" stroke="#555" stroke-width="3" style="view-transition-name:e_GH"/>
<line x1="685" y1="165" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_GI"/>
<line x1="685" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_GJ"/>
<line x1="805" y1="75" x2="918" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_HI"/>
<line x1="918" y1="165" x2="805" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_IJ"/>
<line x1="805" y1="255" x2="955" y2="314" stroke="#555" stroke-width="3" style="view-transition-name:e_JK"/>
<circle cx="220" cy="30" r="24.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<text x="220" y="37" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_A">A</text>
<circle cx="100" cy="102" r="24.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<text x="100" y="109" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_B">B</text>
<circle cx="100" cy="228" r="24.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<text x="100" y="235" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_C">C</text>
<circle cx="220" cy="300" r="24.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<text x="220" y="307" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_D">D</text>
<circle cx="220" cy="165" r="34.0" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<text x="220" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_E">E</text>
<circle cx="490" cy="165" r="30.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<text x="490" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_F">F</text>
<circle cx="685" cy="165" r="32.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<text x="685" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_G">G</text>
<circle cx="805" cy="75" r="26.0" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<text x="805" y="82" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_H">H</text>
<circle cx="918" cy="165" r="28.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<text x="918" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_I">I</text>
<circle cx="805" cy="255" r="28.5" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<text x="805" y="262" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_J">J</text>
<circle cx="955" cy="314" r="22.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="955" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_K">K</text>
</svg>

</div>

<div class="cue">

*E wins, 6.75.*

</div>


---

<!-- _transition: fade 1.6s -->

## The road E–F closes

<hr>

The two pieces drift apart, and every score drops.

<div class="fig">

<svg viewBox="0 0 1080 335" width="1080" height="335" xmlns="http://www.w3.org/2000/svg">
<line x1="168" y1="30" x2="168" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_AE"/>
<line x1="48" y1="102" x2="168" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_BE"/>
<line x1="48" y1="228" x2="168" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_CE"/>
<line x1="168" y1="300" x2="168" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_DE"/>
<line x1="580" y1="165" x2="775" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_FG"/>
<line x1="775" y1="165" x2="895" y2="75" stroke="#555" stroke-width="3" style="view-transition-name:e_GH"/>
<line x1="775" y1="165" x2="1007" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_GI"/>
<line x1="775" y1="165" x2="895" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_GJ"/>
<line x1="895" y1="75" x2="1007" y2="165" stroke="#555" stroke-width="3" style="view-transition-name:e_HI"/>
<line x1="1007" y1="165" x2="895" y2="255" stroke="#555" stroke-width="3" style="view-transition-name:e_IJ"/>
<line x1="895" y1="255" x2="1045" y2="314" stroke="#555" stroke-width="3" style="view-transition-name:e_JK"/>
<circle cx="168" cy="30" r="17.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_A"/>
<text x="168" y="37" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_A">A</text>
<circle cx="48" cy="102" r="17.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_B"/>
<text x="48" y="109" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_B">B</text>
<circle cx="48" cy="228" r="17.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_C"/>
<text x="48" y="235" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_C">C</text>
<circle cx="168" cy="300" r="17.6" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_D"/>
<text x="168" y="307" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_D">D</text>
<circle cx="168" cy="165" r="23.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_E"/>
<text x="168" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_E">E</text>
<circle cx="580" cy="165" r="18.9" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_F"/>
<text x="580" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_F">F</text>
<circle cx="775" cy="165" r="25.3" fill="#B14434" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_G"/>
<text x="775" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_G">G</text>
<circle cx="895" cy="75" r="20.8" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_H"/>
<text x="895" y="82" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_H">H</text>
<circle cx="1007" cy="165" r="23.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_I"/>
<text x="1007" y="172" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_I">I</text>
<circle cx="895" cy="255" r="23.4" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_J"/>
<text x="895" y="262" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_J">J</text>
<circle cx="1045" cy="314" r="18.3" fill="#3959A6" fill-opacity=".85" stroke="#222222" stroke-width="2.5" style="view-transition-name:n_K"/>
<text x="1045" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff" stroke="#222222" stroke-width=".6" style="view-transition-name:t_K">K</text>
</svg>

</div>

<div class="cue">

*G takes over, 4.5. The discs slide; the closed road fades.*

</div>
