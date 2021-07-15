(function ($, Drupal, window, document, undefined) {

  (function ($) {   
    
    //sort blocks on block/add page
    $('.block-system .admin-list li').each(function() {
      label = $(this).find('span.label').text();
      $(this).data('label',label);
    });
    
    $(".block-system .admin-list").each(function(){
      $(this).html($(this).children('li').sort(function(a, b){
          return ($(b).data('label')) < ($(a).data('label')) ? 1 : -1;
      }));
    });    
    
    if($('.block-points-arrows-with-images-form #edit-field-promo-background-color').val() != '_none') {
      $('.block-points-arrows-with-images-form #edit-field-color').val('_none');
      $('.block-points-arrows-with-images-form .form-item-field-color').hide();
    }
    $(".block-points-arrows-with-images-form #edit-field-promo-background-color").change(function () {
      if($('.block-points-arrows-with-images-form #edit-field-promo-background-color').val() != '_none') {
        $('.block-points-arrows-with-images-form #edit-field-color').val('_none');
        $('.block-points-arrows-with-images-form .form-item-field-color').hide();
      }
      if($('.block-points-arrows-with-images-form #edit-field-promo-background-color').val() == '_none') {
        $('.block-points-arrows-with-images-form .form-item-field-color').show();
      }
    });
    
    if($('.block-points-arrows-without-images-form #edit-field-promo-background-color').val() != '_none') {
      $('.block-points-arrows-without-images-form #edit-field-color').val('_none');
      $('.block-points-arrows-without-images-form .form-item-field-color').hide();
    }
    $(".block-points-arrows-without-images-form #edit-field-promo-background-color").change(function () {
      if($('.block-points-arrows-without-images-form #edit-field-promo-background-color').val() != '_none') {
        $('.block-points-arrows-without-images-form #edit-field-color').val('_none');
        $('.block-points-arrows-without-images-form .form-item-field-color').hide();
      }
      if($('.block-points-arrows-without-images-form #edit-field-promo-background-color').val() == '_none') {
        $('.block-points-arrows-without-images-form .form-item-field-color').show();
      }
    });
  
  
  $('form.block-promo-three-form #edit-submit').click(function(e) {
    var promoCount = $('form.block-promo-three-form table .field--name-field-title').length;

    if (promoCount < 2) {
        e.preventDefault();
        alert('Minimum of 2 promos is required. Please add more.')
    }
  });
  
  $('form.block-promo-two-form #edit-submit').click(function(e) {
    var promoCount = $('form.block-promo-two-form table .field--name-field-title').length;

    if (promoCount < 2) {
        e.preventDefault();
        alert('Minimum of 2 promos is required. Please add more.')
    }
  });
  
  $('form.block-points-arrows-with-images-form #edit-submit').click(function(e) {
    var background = $('form.block-points-arrows-with-images-form #edit-field-promo-background-color').val();
    var color = $('form.block-points-arrows-with-images-form #edit-field-color').val();      
    if (background == '_none' && color == '_none') {
        e.preventDefault();
        alert('Please selecte either a Background and Promo Color or Promo Color field value before saving')
    }
     
  });
  
  
    
  $('form.block-promo-one-with-image-form').each(function() {
    var imageRatio = $('form.block-promo-one-with-image-form #edit-field-image-ratio').val();
    if (imageRatio == 'one_into_one_ratio' || imageRatio == 'round') {
      $('form.block-promo-one-with-image-form .field--name-field-choice-style').hide();
    }
  });
  
  $('form.block-promo-one-with-image-form #edit-field-image-ratio').on('change', function() {         
    switch ($('form.block-promo-one-with-image-form #edit-field-image-ratio').val()) {
      case "one_into_one_ratio":
        $('form.block-promo-one-with-image-form .field--name-field-choice-style').hide();
        $('form.block-promo-one-with-image-form #edit-field-choice-style').val('Center-Aligned');          
        break;
      case "round":
        $('form.block-promo-one-with-image-form .field--name-field-choice-style').hide();
        break;
      case "three_into_two_ratio":
        $('form.block-promo-one-with-image-form .field--name-field-choice-style').show();
        break;
      case "two_into_one_ratio":
        $('form.block-promo-one-with-image-form .field--name-field-choice-style').show();
        break;
      default:
        $('form.block-promo-one-with-image-form .field--name-field-choice-style').hide();
        $('form.block-promo-one-with-image-form #edit-field-choice-style').val('Center-Aligned');          
        break;          
    }
  });
    
  $('form.block-promo-one-with-image-form #edit-submit').click(function(e) {
    if ($('form.block-promo-one-with-image-form #edit-field-image-ratio').val() == 'round') {
      $('form.block-promo-one-with-image-form #edit-field-choice-style').val('Center-Aligned');    
    }
  });
    
    /* Remove Master displays in Viewfield select field */
    jQuery('.field--type-viewfield option').each(function( index ) {
      var str = jQuery(this).text();
      if (str.indexOf("Master") >= 0) jQuery(this).detach();
    });
  

  }(jQuery));
})(jQuery, Drupal, this, this.document);


