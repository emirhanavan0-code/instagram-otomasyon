<?php
// Eklentinin kısa kod çıktısını WordPress olmadan üretir (yalnızca reels çekimi için).
// Kullanım: php sayfa.php EKLENTI_KLASORU > sayfa-govde.html
define('ABSPATH', '/');
$E = rtrim($argv[1], '/') . '/';
define('SD_AIG_DIR', $E); define('SD_AIG_URL', '/'); define('SD_AIG_VERSION', 'x');
function add_shortcode() {} function add_action() {} function add_filter() {}
function sd_aig_ayar($k = null) { $a = array('test_url' => 'https://seovedijital.com/yapay-zeka-gorunurluk-testi/', 'web3forms_key' => ''); return $k ? ($a[$k] ?? '') : $a; }
function sd_aig_aktif_saglayicilar() { return array('gemini' => 'Gemini'); } // sitede şu an yalnızca Gemini açık
function get_permalink() { return 'https://seovedijital.com/yapay-zeka-gorunurluk-testi/'; }
function wp_enqueue_script() {} function wp_localize_script() {}
function esc_url_raw($u) { return $u; } function esc_url($u) { return $u; } function rest_url($p) { return '/wp-json/' . $p; }
function home_url($p = '/') { return 'https://seovedijital.com' . $p; }
function is_user_logged_in() { return false; } function wp_create_nonce() { return ''; }
function esc_html($s) { return htmlspecialchars($s, ENT_QUOTES); } function esc_attr($s) { return htmlspecialchars($s, ENT_QUOTES); }
function get_transient($k) { return true; }
function wp_json_encode($d, $f = 0) { return json_encode($d, $f); }
require $E . 'includes/sektorler.php';
require $E . 'includes/kisa-kodlar.php';
echo sd_aig_kisa_kod_arac();
