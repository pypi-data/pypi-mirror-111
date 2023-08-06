// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS("src/libawkward/layoutbuilder/LayoutBuilder.cpp", line)

#include "awkward/layoutbuilder/LayoutBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"
#include "awkward/type/Type.h"
#include "awkward/array/BitMaskedArray.h"
#include "awkward/array/ByteMaskedArray.h"
#include "awkward/array/EmptyArray.h"
#include "awkward/array/IndexedArray.h"
#include "awkward/array/ListArray.h"
#include "awkward/array/ListOffsetArray.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/array/RecordArray.h"
#include "awkward/array/RegularArray.h"
#include "awkward/array/UnionArray.h"
#include "awkward/array/UnmaskedArray.h"

#include "awkward/layoutbuilder/BitMaskedArrayBuilder.h"
#include "awkward/layoutbuilder/ByteMaskedArrayBuilder.h"
#include "awkward/layoutbuilder/EmptyArrayBuilder.h"
#include "awkward/layoutbuilder/IndexedArrayBuilder.h"
#include "awkward/layoutbuilder/IndexedOptionArrayBuilder.h"
#include "awkward/layoutbuilder/ListArrayBuilder.h"
#include "awkward/layoutbuilder/ListOffsetArrayBuilder.h"
#include "awkward/layoutbuilder/NumpyArrayBuilder.h"
#include "awkward/layoutbuilder/RecordArrayBuilder.h"
#include "awkward/layoutbuilder/RegularArrayBuilder.h"
#include "awkward/layoutbuilder/UnionArrayBuilder.h"
#include "awkward/layoutbuilder/UnmaskedArrayBuilder.h"


namespace awkward {

  const std::string
  index_form_to_name(Index::Form form) {
    switch (form) {
    case Index::Form::i8:
      return "int8";
    case Index::Form::u8:
      return "uint8";
    case Index::Form::i32:
      return "int32";
    case Index::Form::u32:
      return "uint32";
    case Index::Form::i64:
      return "int64";
    default:
      throw std::runtime_error(
        std::string("unrecognized Index::Form ") + FILENAME(__LINE__));
    }
  }

  const std::string
  index_form_to_vm_format(Index::Form form) {
    switch (form) {
    case Index::Form::i8:
      return "b";
    case Index::Form::u8:
      return "B";
    case Index::Form::i32:
      return "i";
    case Index::Form::u32:
      return "I";
    case Index::Form::i64:
      return "q";
    default:
      throw std::runtime_error(
        std::string("unrecognized Index::Form ") + FILENAME(__LINE__));
    }
  }

  const std::string
  dtype_to_state(util::dtype dt) {
    switch (dt) {
    case util::dtype::boolean:
      return std::to_string(static_cast<utype>(state::boolean));
    case util::dtype::int8:
      return std::to_string(static_cast<utype>(state::int8));
    case util::dtype::int16:
      return std::to_string(static_cast<utype>(state::int16));
    case util::dtype::int32:
      return std::to_string(static_cast<utype>(state::int32));
    case util::dtype::int64:
      return std::to_string(static_cast<utype>(state::int64));
    case util::dtype::uint8:
      return std::to_string(static_cast<utype>(state::uint8));
    case util::dtype::uint16:
      return std::to_string(static_cast<utype>(state::uint16));
    case util::dtype::uint32:
      return std::to_string(static_cast<utype>(state::uint32));
    case util::dtype::uint64:
      return std::to_string(static_cast<utype>(state::uint64));
    case util::dtype::float16:
      return std::to_string(static_cast<utype>(state::float16));
    case util::dtype::float32:
      return std::to_string(static_cast<utype>(state::float32));
    case util::dtype::float64:
      return std::to_string(static_cast<utype>(state::float64));
    case util::dtype::float128:
      return std::to_string(static_cast<utype>(state::float128));
    case util::dtype::complex64:
      return std::to_string(static_cast<utype>(state::complex64));
    case util::dtype::complex128:
      return std::to_string(static_cast<utype>(state::complex128));
    case util::dtype::complex256:
      return std::to_string(static_cast<utype>(state::complex256));
      // case datetime64:
      //   return static_cast<utype>(state::datetime64);
      // case timedelta64:
      //   return static_cast<utype>(state::timedelta64);
    default:
      throw std::runtime_error(
        std::string("unrecognized util::dtype ") + FILENAME(__LINE__));
    }
  };

  const std::string
  dtype_to_vm_format(util::dtype dt) {
    switch (dt) {
    case util::dtype::boolean:
      return "?";
    case util::dtype::int8:
      return "b";
    case util::dtype::int16:
      return "h";
    case util::dtype::int32:
      return "i";
    case util::dtype::int64:
      return "q";
    case util::dtype::uint8:
      return "B";
    case util::dtype::uint16:
      return "H";
    case util::dtype::uint32:
      return "I";
    case util::dtype::uint64:
      return "Q";
    case util::dtype::float16:
    case util::dtype::float32:
      return "f";
    case util::dtype::float64:
    case util::dtype::float128:
    case util::dtype::complex64:
    case util::dtype::complex128:
    case util::dtype::complex256:
 // case datetime64:
 // case timedelta64:
      return "d";
    default:
      throw std::runtime_error(
        std::string("unrecognized util::dtype ") + FILENAME(__LINE__));
    }
  };

  int64_t LayoutBuilder::next_node_id = 0;
  int64_t LayoutBuilder::error_id = 0;

  LayoutBuilder::LayoutBuilder(const FormPtr& form,
                                       const ArrayBuilderOptions& options,
                                       bool vm_init)
    : initial_(options.initial()),
      length_(8),
      builder_(formBuilderFromA(form)),
      vm_(nullptr),
      vm_input_data_("data"),
      vm_source_() {
    LayoutBuilder::error_id = 0;
    vm_source_ = std::string("variable err").append("\n");
    vm_source_.append("input ")
      .append(vm_input_data_).append("\n");

    vm_source_.append(builder_.get()->vm_error()).append("\n");
    vm_source_.append(builder_.get()->vm_output()).append("\n");
    vm_source_.append(builder_.get()->vm_func()).append("\n");
    vm_source_.append(builder_.get()->vm_from_stack()).append("\n");

    vm_source_.append("0").append("\n")
      .append("begin").append("\n")
      .append("pause").append("\n")
      .append(builder_.get()->vm_func_name()).append("\n")
      .append("1+").append("\n")
      .append("again").append("\n");

    if (vm_init) {
      initialise();
    }
  }

  FormBuilderPtr
  LayoutBuilder::formBuilderFromA(const FormPtr& form) {
    if (auto const& downcasted_form = std::dynamic_pointer_cast<BitMaskedForm>(form)) {
      return std::make_shared<BitMaskedArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<ByteMaskedForm>(form)) {
      return std::make_shared<ByteMaskedArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<EmptyForm>(form)) {
      return std::make_shared<EmptyArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<IndexedForm>(form)) {
      switch (downcasted_form.get()->index()) {
      // case Index::Form::i8:
      // case Index::Form::u8:
      case Index::Form::i32:
      case Index::Form::u32:
      case Index::Form::i64:
      default:
        return std::make_shared<IndexedArrayBuilder>(downcasted_form);
      };
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<IndexedOptionForm>(form)) {
      return std::make_shared<IndexedOptionArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<ListForm>(form)) {
      return std::make_shared<ListArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<ListOffsetForm>(form)) {
      return std::make_shared<ListOffsetArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<NumpyForm>(form)) {
      return std::make_shared<NumpyArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<RecordForm>(form)) {
      return std::make_shared<RecordArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<RegularForm>(form)) {
      return std::make_shared<RegularArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<UnionForm>(form)) {
      return std::make_shared<UnionArrayBuilder>(downcasted_form);
    }
    else if (auto const& downcasted_form = std::dynamic_pointer_cast<UnmaskedForm>(form)) {
      return std::make_shared<UnmaskedArrayBuilder>(downcasted_form);
    }
    else {
      throw std::invalid_argument(
        std::string("LayoutBuilder does not recognise the Form ")
        + FILENAME(__LINE__));
    }
  }

  void
  LayoutBuilder::connect(const std::shared_ptr<ForthMachine32>& vm) {
    if (vm_ == nullptr) {
      vm_ = vm;

      std::shared_ptr<void> ptr(
        kernel::malloc<void>(kernel::lib::cpu, 8*sizeof(uint8_t)));

      vm_inputs_map_[vm_input_data_] = std::make_shared<ForthInputBuffer>(ptr, 0, 8);
      vm_.get()->run(vm_inputs_map_);
    }
    else {
      throw std::invalid_argument(
        std::string("LayoutBuilder is already connected to a Virtual Machine ")
        + FILENAME(__LINE__));
    }
  }

  void
  LayoutBuilder::initialise() {
    vm_ = std::make_shared<ForthMachine32>(vm_source());

    std::shared_ptr<void> ptr(
      kernel::malloc<void>(kernel::lib::cpu, initial_*(int64_t)sizeof(uint8_t)));

    vm_inputs_map_[vm_input_data_] = std::make_shared<ForthInputBuffer>(ptr, 0, initial_);
    vm_.get()->run(vm_inputs_map_);
  }

  template<typename T>
  void
  LayoutBuilder::set_data(T x) {
    reinterpret_cast<T*>(vm_inputs_map_[vm_input_data_]->ptr().get())[0] = x;
  }

  void
  LayoutBuilder::resume() const {
    if (vm_.get()->resume() == util::ForthError::user_halt) {
      throw std::invalid_argument(vm_.get()->string_at(vm_.get()->stack().back()));
    }
  }

  void
  LayoutBuilder::debug_step() const {
    std::cout << "stack ";
    for (auto const& i : vm_.get()->stack()) {
      std::cout << i << ", ";
    }
    std::cout << "\n";
    for (auto const& i : vm_.get()->outputs()) {
      std::cout << i.first << " : ";
      std::cout << i.second.get()->toNumpyArray().get()->tostring();
      std::cout << "\n";
    }
    std::cout << "array:\n" << snapshot().get()->tostring() << "\n";
  }

  const FormPtr
  LayoutBuilder::form() const {
    return builder_.get()->form();
  }

  const std::string
  LayoutBuilder::vm_source() const {
    return vm_source_;
  }

  const std::string
  LayoutBuilder::tostring() const {
    util::TypeStrs typestrs;
    typestrs["char"] = "char";
    typestrs["string"] = "string";
    std::stringstream out;
    out << "<LayoutBuilder length=\"" << length() << "\" type=\""
        << type(typestrs).get()->tostring() << "\"/>";
    return out.str();
  }

  int64_t
  LayoutBuilder::next_id() {
    return LayoutBuilder::next_node_id++;
  }

  int64_t
  LayoutBuilder::next_error_id() {
    return LayoutBuilder::error_id++;
  }

  int64_t
  LayoutBuilder::length() const {
    return length_;
  }

  const TypePtr
  LayoutBuilder::type(const util::TypeStrs& typestrs) const {
    return builder_.get()->snapshot(vm_.get()->outputs()).get()->type(typestrs);
  }

  const ContentPtr
  LayoutBuilder::snapshot() const {
    vm_.get()->maybe_throw(util::ForthError::user_halt, ignore_);
    return builder_.get()->snapshot(vm_.get()->outputs());
  }

  const ContentPtr
  LayoutBuilder::getitem_at(int64_t at) const {
    return snapshot().get()->getitem_at(at);
  }

  const ContentPtr
  LayoutBuilder::getitem_range(int64_t start, int64_t stop) const {
    return snapshot().get()->getitem_range(start, stop);
  }

  const ContentPtr
  LayoutBuilder::getitem_field(const std::string& key) const {
    return snapshot().get()->getitem_field(key);
  }

  const ContentPtr
  LayoutBuilder::getitem_fields(const std::vector<std::string>& keys) const {
    return snapshot().get()->getitem_fields(keys);
  }

  const ContentPtr
  LayoutBuilder::getitem(const Slice& where) const {
    return snapshot().get()->getitem(where);
  }

  void
  LayoutBuilder::null() {
    vm_.get()->stack_push(static_cast<utype>(state::null));
    resume();
  }

  void
  LayoutBuilder::boolean(bool x) {
    builder_.get()->boolean(x, this);
  }

  template<>
  void
  LayoutBuilder::add<bool>(bool x) {
    set_data<bool>(x);
    vm_.get()->stack_push(static_cast<utype>(state::boolean));
    resume();
  }

  void
  LayoutBuilder::int64(int64_t x) {
    builder_.get()->int64(x, this);
  }

  template<>
  void
  LayoutBuilder::add<int64_t>(int64_t x) {
    set_data<int64_t>(x);
    vm_.get()->stack_push(static_cast<utype>(state::int64));
    resume();
  }

  void
  LayoutBuilder::float64(double x) {
    builder_.get()->float64(x, this);
  }

  template<>
  void
  LayoutBuilder::add<double>(double x) {
    set_data<double>(x);
    vm_.get()->stack_push(static_cast<utype>(state::float64));
    resume();
  }

  void
  LayoutBuilder::complex(std::complex<double> x) {
    builder_.get()->complex(x, this);
  }

  template<>
  void
  LayoutBuilder::add<std::complex<double>>(std::complex<double> x) {
    set_data<std::complex<double>>(x);
    vm_.get()->stack_push(static_cast<utype>(state::complex128));
    resume();
  }

  void
  LayoutBuilder::bytestring(const char* x) {
    throw std::runtime_error(
      std::string("LayoutBuilder a null terminated 'bytestring' is not implemented yet")
      + FILENAME(__LINE__));
  }

  void
  LayoutBuilder::bytestring(const char* x, int64_t length) {
    for (int64_t i = 0; i < length; i++) {
      set_data<uint8_t>((uint8_t)x[i]);
      vm_.get()->stack_push(static_cast<utype>(state::uint8));
      resume();
    }
  }

  void
  LayoutBuilder::bytestring(const std::string& x) {
    builder_.get()->bytestring(x, this);
  }

  void
  LayoutBuilder::string(const char* x) {
    throw std::runtime_error(
      std::string("LayoutBuilder a null terminated 'string' is not implemented yet")
      + FILENAME(__LINE__));
  }

  void
  LayoutBuilder::string(const char* x, int64_t length) {
    for (int64_t i = 0; i < length; i++) {
      set_data<uint8_t>((uint8_t)x[i]);
      vm_.get()->stack_push(static_cast<utype>(state::uint8));
      resume();
    }
  }

  void
  LayoutBuilder::string(const std::string& x) {
    builder_.get()->string(x, this);
  }

  template<>
  void
  LayoutBuilder::add<const std::string&>(const std::string& x) {
    begin_list();
    string(x.c_str(), (int64_t)x.length());
    end_list();
  }

  void
  LayoutBuilder::begin_list() {
    builder_.get()->begin_list(this);
  }

  void
  LayoutBuilder::add_begin_list() {
    vm_.get()->stack_push(static_cast<utype>(state::begin_list));
    vm_.get()->resume();
  }

  void
  LayoutBuilder::end_list() {
    builder_.get()->end_list(this);
  }

  void
  LayoutBuilder::add_end_list() {
    vm_.get()->stack_push(static_cast<utype>(state::end_list));
    vm_.get()->resume();
  }

  void
  LayoutBuilder::index(int64_t x) {
    vm_.get()->stack_push((int32_t)x);
    vm_.get()->stack_push(static_cast<utype>(state::index));
    vm_.get()->resume();
  }

  void
  LayoutBuilder::tag(int8_t x) {
    set_data<int8_t>(x);
    vm_.get()->stack_push(static_cast<utype>(state::tag));
    vm_.get()->resume();
  }

}
